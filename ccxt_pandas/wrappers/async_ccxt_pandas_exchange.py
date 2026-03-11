import asyncio
import inspect
from functools import wraps
from typing import Literal, Callable, Union, Any
from asyncio import Semaphore

import ccxt.pro as ccxt
import pandas as pd
from dataclasses import dataclass, field

from async_lru import alru_cache

from ccxt_pandas.wrappers.base_processor import BaseProcessor
from ccxt_pandas.wrappers.method_mappings import (
    single_order_methods,
    symbol_order_methods,
    modified_methods,
)
from ccxt_pandas.utils.async_ccxt_pandas_exchange_typed import (
    AsyncCCXTPandasExchangeTyped,
)
from ccxt_pandas.utils.pandas_utils import (
    preprocess_order,
    preprocess_order_dataframe,
    check_orders_dataframe_size,
    create_full_async_tasks,
    create_multi_symbol_async_tasks,
    create_full_multi_symbol_async_tasks,
    async_loop_through_orders,
    async_call_per_group_concat,
    async_concat_results,
    concat_results,
    FunctionHandler,
    timestamp_to_int,
)
from ccxt_pandas.utils.utils import exchange_has_method


@dataclass
class AsyncCCXTPandasExchange(AsyncCCXTPandasExchangeTyped):
    """
    An asynchronous wrapper class for CCXT Pro Exchange that integrates pandas for enhanced
    data handling and provides preprocessing utilities for working with cryptocurrency trading data.

    Supports advanced features including:
    - Multi-symbol operations: pass a list of symbols to create concurrent async tasks
    - Date range pagination: use from_date/to_date to create paginated async task lists
    - Order DataFrame batching: use _from_dataframe methods to batch async order operations
    - Semaphore-based concurrency control
    - Error handling modes: "raise", "warn", or "ignore" errors from exchange calls

    Methods always return coroutines. Multi-symbol and paginated calls are gathered
    and concatenated internally via async_concat_results().

    Note: the cache=True parameter available on the sync wrapper is not supported here.
    For incremental local caching in async contexts, manage a DataFrame externally and
    pass it to async_concat_results().

    Attributes:
        exchange (ccxt.Exchange): The CCXT Pro exchange instance.
        exchange_name (str | None): The name of the exchange.
        account_name (str | None): The account name for tracking.
        dropna_fields (bool): Whether to remove all-NaN columns.
        attach_trades_to_orders (bool): Whether to attach trades to orders.
        max_order_cost (float): Maximum cost for a single order.
        max_number_of_orders (int): Maximum number of orders in batch operations.
        markets_cache_time (int): Cache duration for market data in seconds.
        errors (str): Error handling mode: "raise", "warn", or "ignore".
        cost_out_of_range (str): Behavior when cost exceeds ranges: "warn" or "clip".
        amount_out_of_range (str): Behavior when amount exceeds ranges: "warn" or "clip".
        price_out_of_range (str): Behavior when price exceeds ranges: "warn" or "clip".
        semaphore_value (int): Concurrency limit for async operations.
    """

    exchange: ccxt.Exchange
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
    semaphore_value: int = 1000
    _ccxt_processor: BaseProcessor = field(
        default_factory=BaseProcessor, init=False, repr=False
    )
    _function_handler: FunctionHandler = field(
        default_factory=FunctionHandler, init=False, repr=False
    )
    _semaphore: Semaphore = field(default_factory=Semaphore, init=False, repr=False)
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
        self._semaphore = Semaphore(self.semaphore_value)
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
        async def base_call(
            *args, **kwargs
        ) -> Union[dict, pd.DataFrame, asyncio.Future]:
            if method_name in single_order_methods:
                kwargs["amount"], kwargs["price"] = preprocess_order(
                    exchange=self.exchange,
                    symbol=kwargs["symbol"],
                    order_type=kwargs["type"],
                    amount=kwargs.get("amount"),
                    price=kwargs.get("price"),
                    cost=kwargs.get("cost"),
                    markets=await self.load_cached_markets(),
                    max_cost=self.max_order_cost,
                    cost_out_of_range=self.cost_out_of_range,
                    price_out_of_range=self.price_out_of_range,
                    amount_out_of_range=self.amount_out_of_range,
                )
                if "cost" in kwargs:
                    kwargs.pop("cost")
            elif method_name in symbol_order_methods:
                kwargs["orders"] = kwargs["orders"][["id", "symbol"]].to_dict("records")
            if "since" in kwargs:
                kwargs["since"] = timestamp_to_int(kwargs["since"])
            async with self._semaphore:
                if asyncio.iscoroutinefunction(original_method):
                    result = await original_method(*args, **kwargs)
                else:
                    result = original_method(*args, **kwargs)
                return self._ccxt_processor.preprocess_outputs(
                    method_name=method_name,
                    result=result,
                    symbol=kwargs.get("symbol"),
                )

        return base_call

    def __getattribute__(self, method_name: str) -> Callable:
        if method_name not in modified_methods | {"close"}:
            return super().__getattribute__(method_name)

        base_call = self._make_base_call(method_name)
        param_names = self._analyze_method_signature(method_name)

        supports_symbol = "symbol" in param_names
        supports_code = "code" in param_names
        supports_since = "since" in param_names

        async def wrapper(*args, **kwargs) -> pd.DataFrame | None | Any:
            symbols = kwargs.pop("symbol", kwargs.pop("code", []))
            if not isinstance(symbols, (list, tuple, set)):
                symbols = [symbols]
            from_date = kwargs.pop("from_date", None)
            to_date = kwargs.pop("to_date", None)
            if symbols and (supports_symbol or supports_code):
                symbol_column: Literal["code", "symbol"] = (
                    "code" if supports_code else "symbol"
                )
                if supports_since and from_date:
                    tasks = create_full_multi_symbol_async_tasks(
                        function=base_call,
                        symbols=symbols,
                        symbol_column=symbol_column,
                        from_date=from_date,
                        to_date=to_date,
                        **kwargs,
                    )
                else:
                    tasks = create_multi_symbol_async_tasks(
                        function=base_call,
                        symbols=symbols,
                        symbol_column=symbol_column,
                        **kwargs,
                    )
                return await async_concat_results(tasks)
            elif supports_since and from_date:
                tasks = create_full_async_tasks(
                    function=base_call,
                    symbols=symbols,
                    from_date=from_date,
                    to_date=to_date,
                    **kwargs,
                )
                return await async_concat_results(tasks)
            return await self._function_handler.async_try_function(
                base_call(*args, **kwargs)
            )

        return wrapper

    async def create_order_from_dataframe(
        self, orders: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        base_call = self._make_base_call("create_order")
        tasks = async_loop_through_orders(
            function=base_call,
            orders=orders,
            max_number_of_orders=self.max_number_of_orders,
            **kwargs,
        )
        return await async_concat_results(tasks)

    async def edit_order_from_dataframe(
        self, orders: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        base_call = self._make_base_call("edit_order")
        tasks = async_loop_through_orders(
            function=base_call,
            orders=orders,
            max_number_of_orders=self.max_number_of_orders,
            **kwargs,
        )
        return await async_concat_results(tasks)

    async def cancel_order_from_dataframe(
        self, orders: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        base_call = self._make_base_call("cancel_order")
        tasks = async_loop_through_orders(
            function=base_call,
            orders=orders,
            max_number_of_orders=self.max_number_of_orders,
            **kwargs,
        )
        return await async_concat_results(tasks)

    async def create_orders_from_dataframe(
        self, orders: pd.DataFrame, chunk_size: int = 5, **kwargs
    ) -> pd.DataFrame:
        orders = preprocess_order_dataframe(
            orders=orders,
            markets=await self.load_cached_markets(),
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
        tasks = []
        for i in range(0, len(order_dicts), chunk_size):
            chunk = order_dicts[i : i + chunk_size]
            tasks.append(base_call(orders=chunk, **kwargs))
        return await async_concat_results(tasks)

    async def edit_orders_from_dataframe(
        self, orders: pd.DataFrame, chunk_size: int = 5, **kwargs
    ) -> pd.DataFrame:
        orders = preprocess_order_dataframe(
            orders=orders,
            markets=await self.load_cached_markets(),
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
        tasks = []
        for i in range(0, len(order_dicts), chunk_size):
            chunk = order_dicts[i : i + chunk_size]
            tasks.append(base_call(orders=chunk, **kwargs))
        return await async_concat_results(tasks)

    async def cancel_orders_from_dataframe(
        self, orders: pd.DataFrame, **kwargs
    ) -> pd.DataFrame:
        base_call = self._make_base_call("cancel_orders")
        tasks = async_call_per_group_concat(
            function=base_call,
            orders=orders,
            **kwargs,
        )
        return await async_concat_results(tasks)

    async def load_cached_markets(self, params: dict | None = None) -> pd.DataFrame:

        @alru_cache(ttl=self.markets_cache_time)
        async def _cached_load_markets() -> pd.DataFrame:
            async with self._semaphore:
                return await self.load_markets(reload=True, params=params or {})

        return await _cached_load_markets()

    def has_method(self, method_name: str) -> bool:
        return exchange_has_method(self.exchange, method_name)
