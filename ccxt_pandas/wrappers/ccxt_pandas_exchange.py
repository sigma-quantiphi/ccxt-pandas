import inspect
from functools import wraps
from typing import Literal, Callable, Union, Any

import ccxt
import pandas as pd
from dataclasses import dataclass, field

from cachetools.func import ttl_cache

from ccxt_pandas.wrappers.base_processor import BaseProcessor
from ccxt_pandas.wrappers.method_mappings import (
    single_order_methods,
    symbol_order_methods,
    modified_methods,
)
from ccxt_pandas.utils.ccxt_pandas_exchange_typed import CCXTPandasExchangeTyped
from ccxt_pandas.utils.pandas_utils import (
    preprocess_order,
    preprocess_order_dataframe,
    check_orders_dataframe_size,
    concat_results,
    FunctionHandler,
    merge_markets_with_balances,
)
from ccxt_pandas.utils.utils import exchange_has_method


@dataclass
class CCXTPandasExchange(CCXTPandasExchangeTyped):
    """
    CCXTPandasExchange is a wrapper for the CCXT library that integrates with Pandas
    to provide streamlined data processing for cryptocurrency exchanges. It enables users
    to seamlessly create orders, fetch market data, and process exchange responses as
    Pandas DataFrames.

    Supports advanced features including:
    - Multi-symbol operations: pass a list of symbols to fetch data for all at once
    - Date range pagination: use from_date/to_date to paginate through historical data
    - Caching: use cache=True to incrementally build a local cache of fetched data
    - Order DataFrame batching: use _from_dataframe methods to batch order operations
    - Error handling modes: "raise", "warn", or "ignore" errors from exchange calls

    Attributes:
        exchange (ccxt.Exchange): An instance of the CCXT exchange client.
        exchange_name (str | None): The name of the exchange to interact with.
        account_name (str | None): The account name, if required for tracking.
        dropna_fields (bool): Determines whether empty (NaN) columns are removed from DataFrame outputs.
        attach_trades_to_orders (bool): Determines whether trades are attached to orders when processing orders.
        max_order_cost (float): Maximum cost value for any single order.
        max_number_of_orders (int): Maximum number of orders to process in a single operation.
        markets_cache_time (int): Cache duration (in seconds) for markets data.
        errors (str): Error handling mode: "raise", "warn", or "ignore".
        cost_out_of_range (str): Behavior when cost exceeds ranges: "warn" or "clip".
        amount_out_of_range (str): Behavior when amount exceeds ranges: "warn" or "clip".
        price_out_of_range (str): Behavior when price exceeds ranges: "warn" or "clip".
    """

    exchange: ccxt.Exchange = field(default_factory=ccxt.binance)
    exchange_name: str | None = None
    account_name: str | None = None
    dropna_fields: bool = True
    attach_trades_to_orders: bool = False
    max_order_cost: float = 10_000
    max_number_of_orders: int = 1_000
    markets_cache_time: int = 3600
    errors: Literal["ignore", "raise", "warn"] = "raise"
    cost_out_of_range: Literal["warn", "clip"] = "warn"
    amount_out_of_range: Literal["warn", "clip"] = "warn"
    price_out_of_range: Literal["warn", "clip"] = "warn"
    validate_schemas: bool = False
    strict_validation: bool = False
    _ccxt_processor: BaseProcessor = field(default_factory=BaseProcessor, init=False, repr=False)
    _function_handler: FunctionHandler = field(default_factory=FunctionHandler, init=False, repr=False)
    _signature_cache: dict = field(default_factory=dict, init=False, repr=False)

    def __post_init__(self):
        if self.exchange_name is None:
            self.exchange_name = self.exchange.id
        self._ccxt_processor = BaseProcessor(
            exchange_name=self.exchange_name,
            account_name=self.account_name,
            dropna_fields=self.dropna_fields,
            attach_trades_to_orders=self.attach_trades_to_orders,
            cost_out_of_range=self.cost_out_of_range,
            amount_out_of_range=self.amount_out_of_range,
            price_out_of_range=self.price_out_of_range,
            validate_schemas=self.validate_schemas,
            strict_validation=self.strict_validation,
        )
        self._function_handler = FunctionHandler(errors=self.errors)

    def _analyze_method_signature(self, name: str) -> dict:
        if name not in self._signature_cache:
            exchange = super().__getattribute__("exchange")
            func = getattr(exchange, name)
            sig = inspect.signature(func)
            self._signature_cache[name] = sig.parameters
        return self._signature_cache[name]

    def _make_base_call(self, method_name: str):
        original_method = getattr(self.exchange, method_name)

        @wraps(original_method)
        def base_call(*args, **kwargs) -> Union[dict, pd.DataFrame]:
            if method_name in single_order_methods:
                kwargs["amount"], kwargs["price"] = preprocess_order(
                    exchange=self.exchange,
                    symbol=kwargs["symbol"],
                    order_type=kwargs["type"],
                    amount=kwargs.get("amount"),
                    price=kwargs.get("price"),
                    cost=kwargs.get("cost"),
                    markets=self.load_cached_markets(),
                    max_cost=self.max_order_cost,
                    cost_out_of_range=self.cost_out_of_range,
                    amount_out_of_range=self.amount_out_of_range,
                    price_out_of_range=self.price_out_of_range,
                )
                if "cost" in kwargs:
                    kwargs.pop("cost")
            elif method_name in symbol_order_methods:
                kwargs["orders"] = kwargs["orders"][["id", "symbol"]].to_dict("records")
            result = original_method(*args, **kwargs)
            result = self._ccxt_processor.preprocess_outputs(
                method_name=method_name, result=result, symbol=kwargs.get("symbol")
            )
            return result

        return base_call

    def __getattribute__(self, method_name: str) -> Callable:
        if method_name not in modified_methods:
            return super().__getattribute__(method_name)

        param_names = self._analyze_method_signature(method_name)
        base_call = self._make_base_call(method_name)

        supports_symbol = "symbol" in param_names
        supports_code = "code" in param_names
        supports_since = "since" in param_names

        def wrapper(*args, **kwargs) -> pd.DataFrame | None | Any:
            cache = kwargs.pop("cache", False)
            symbols = kwargs.pop("symbol", kwargs.pop("code", []))
            if not isinstance(symbols, (list, tuple, set)):
                symbols = [symbols]
            from_date = kwargs.pop("from_date", None)
            to_date = kwargs.pop("to_date", None)

            if symbols and (supports_symbol or supports_code):
                symbol_column: Literal["code", "symbol"] = (
                    "code" if supports_code else "symbol"
                )
                if cache:
                    cache_attr = method_name.replace("fetch_", "")
                    try:
                        current_cache = object.__getattribute__(self, cache_attr)
                    except AttributeError:
                        current_cache = pd.DataFrame()
                    updated = (
                        self._function_handler.load_multi_symbol_dataset_into_cache(
                            function=base_call,
                            data=current_cache,
                            symbols=symbols,
                            symbol_column=symbol_column,
                            from_date=from_date,
                            to_date=to_date,
                            **kwargs,
                        )
                    )
                    setattr(self, cache_attr, updated)
                    return updated.copy()
                elif supports_since and from_date:
                    return self._function_handler.load_full_multi_symbol_dataset(
                        function=base_call,
                        symbols=symbols,
                        symbol_column=symbol_column,
                        from_date=from_date,
                        to_date=to_date,
                        **kwargs,
                    )
                else:
                    return self._function_handler.load_multi_symbol_dataset(
                        function=base_call,
                        symbols=symbols,
                        symbol_column=symbol_column,
                        **kwargs,
                    )
            elif supports_since and from_date:
                if cache:
                    cache_attr = method_name.replace("fetch_", "")
                    try:
                        current_cache = object.__getattribute__(self, cache_attr)
                    except AttributeError:
                        current_cache = pd.DataFrame()
                    updated = self._function_handler.load_dataset_into_cache(
                        function=base_call,
                        data=current_cache,
                        symbols=symbols,
                        from_date=from_date,
                        to_date=to_date,
                        **kwargs,
                    )
                    setattr(self, cache_attr, updated)
                    return updated.copy()
                else:
                    return self._function_handler.load_full_dataset(
                        function=base_call,
                        symbols=symbols,
                        from_date=from_date,
                        to_date=to_date,
                        **kwargs,
                    )
            return self._function_handler.try_function(function=base_call, **kwargs)

        return wrapper

    def create_order_from_dataframe(
        self, orders: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        base_call = self._make_base_call("create_order")
        return self._function_handler.loop_through_orders(
            function=base_call,
            orders=orders,
            max_number_of_orders=self.max_number_of_orders,
            **kwargs,
        )

    def edit_order_from_dataframe(self, orders: pd.DataFrame, **kwargs) -> pd.DataFrame:
        base_call = self._make_base_call("edit_order")
        return self._function_handler.loop_through_orders(
            function=base_call,
            orders=orders,
            max_number_of_orders=self.max_number_of_orders,
            **kwargs,
        )

    def cancel_order_from_dataframe(
        self, orders: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        base_call = self._make_base_call("cancel_order")
        return self._function_handler.loop_through_orders(
            function=base_call,
            orders=orders,
            max_number_of_orders=self.max_number_of_orders,
            **kwargs,
        )

    def create_orders_from_dataframe(
        self, orders: pd.DataFrame, chunk_size: int = 5, **kwargs
    ) -> pd.DataFrame:
        orders = preprocess_order_dataframe(
            orders=orders,
            markets=self.load_cached_markets(),
            max_orders=self.max_number_of_orders,
            max_cost=self.max_order_cost,
            cost_out_of_range=self.cost_out_of_range,
            amount_out_of_range=self.amount_out_of_range,
            price_out_of_range=self.price_out_of_range,
        )
        order_dicts = self._ccxt_processor.orders_to_dict(
            orders=orders,
            exchange=self.exchange,
        )
        base_call = self._make_base_call("create_orders")
        results = []
        for i in range(0, len(order_dicts), chunk_size):
            chunk = order_dicts[i : i + chunk_size]
            result = self._function_handler.try_function(
                function=base_call,
                orders=chunk,
                **kwargs,
            )
            results.append(result)
        return concat_results(results)

    def edit_orders_from_dataframe(
        self, orders: pd.DataFrame, chunk_size: int = 5, **kwargs
    ) -> pd.DataFrame:
        orders = preprocess_order_dataframe(
            orders=orders,
            markets=self.load_cached_markets(),
            max_orders=self.max_number_of_orders,
            max_cost=self.max_order_cost,
            cost_out_of_range=self.cost_out_of_range,
            amount_out_of_range=self.amount_out_of_range,
            price_out_of_range=self.price_out_of_range,
        )
        order_dicts = self._ccxt_processor.orders_to_dict(
            orders=orders,
            exchange=self.exchange,
        )
        base_call = self._make_base_call("edit_orders")
        results = []
        for i in range(0, len(order_dicts), chunk_size):
            chunk = order_dicts[i : i + chunk_size]
            result = self._function_handler.try_function(
                function=base_call,
                orders=chunk,
                **kwargs,
            )
            results.append(result)
        return concat_results(results)

    def cancel_orders_from_dataframe(
        self, orders: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        base_call = self._make_base_call("cancel_orders")
        return self._function_handler.call_per_group_concat(
            function=base_call,
            orders=orders,
            **kwargs,
        )

    def load_cached_markets(self, params: dict | None = None) -> pd.DataFrame:
        @ttl_cache(ttl=self.markets_cache_time)
        def _cached_load_markets() -> pd.DataFrame:
            return self.load_markets(reload=True, params=params or {})

        return _cached_load_markets()

    def fetch_markets_with_balances(
        self,
        markets_params: dict | None = None,
        balance_params: dict | None = None,
        reload_markets: bool = False,
    ) -> pd.DataFrame:
        return merge_markets_with_balances(
            markets=self.load_markets(
                params=markets_params or {}, reload=reload_markets
            ),
            balance=self.fetch_balance(params=balance_params or {}),
        )

    def has_method(self, method_name: str) -> bool:
        return exchange_has_method(self.exchange, method_name)
