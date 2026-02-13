import asyncio
import warnings
from dataclasses import dataclass
from typing import Literal, Awaitable, Any, Callable, Union, overload

import ccxt
import numpy as np
import pandas as pd
import pandera.pandas as pa
from pandas import DataFrame

cap_zero_columns = ["limits_price.min", "limits_cost.min", "limits_amount.min"]
cap_inf_columns = ["limits_price.max", "limits_cost.max", "limits_amount.max"]
order_data_columns = ["symbol"] + cap_zero_columns + cap_inf_columns


@overload
def format_timestamp(timestamp: None) -> None: ...


@overload
def format_timestamp(timestamp: int | pd.Timestamp | dict | str) -> pd.Timestamp: ...


def format_timestamp(
    timestamp: int | pd.Timestamp | dict | str | None,
) -> pd.Timestamp | None:
    now = pd.Timestamp.now(tz="UTC")
    if isinstance(timestamp, dict):
        timestamp = now + pd.DateOffset(**timestamp)
    elif isinstance(timestamp, str):
        timestamp = now + pd.Timedelta(timestamp)
    return timestamp


def timestamp_to_int(timestamp: int | pd.Timestamp | dict | str | None) -> int:
    timestamp = format_timestamp(timestamp)
    if isinstance(timestamp, pd.Timestamp):
        timestamp = int(timestamp.timestamp() * 1000)
    return timestamp


def date_time_fields_to_int_str(data: dict) -> dict:
    def transform_value(value):
        if isinstance(value, pd.Timestamp):
            return str(int(value.timestamp() * 1000))
        elif isinstance(value, dict):
            return date_time_fields_to_int_str(value)
        elif isinstance(value, list):
            return [transform_value(v) for v in value]
        return value

    return {key: transform_value(value) for key, value in data.items()}


def date_time_columns_to_int_str(data: pd.DataFrame) -> pd.DataFrame:
    columns = (
        data.select_dtypes("datetimetz").columns.tolist()
        + data.select_dtypes("datetime").columns.tolist()
    )
    data[columns] = (data[columns].astype("int64") // 10**6).astype(str)
    return data


def expand_dict_columns(data: pd.DataFrame, separator: str = ".") -> pd.DataFrame:
    data = data.reset_index(drop=True)
    dict_columns = [
        x for x in data.columns if any(data[x].apply(lambda y: isinstance(y, dict)))
    ]
    columns_list = [data.drop(columns=dict_columns).copy()]
    for dict_column in dict_columns:
        exploded_column = pd.json_normalize(data[dict_column])
        exploded_column.columns = [
            f"{dict_column}{separator}{x}" for x in exploded_column.columns
        ]
        columns_list.append(exploded_column.copy())
    return pd.concat(columns_list, axis=1)


def determine_mandatory_optional_fields_pandera(model: pa.DataFrameModel) -> dict:
    schema = model.to_schema()
    fields = {"mandatory": [], "optional": []}
    for col_name, col_obj in schema.columns.items():
        if col_obj.nullable:
            fields["optional"].append(col_name)
        else:
            fields["mandatory"].append(col_name)
    return fields


def combine_params(row: pd.Series, param_cols: list) -> dict:
    return {
        column.replace("params.", ""): row[column]
        for column in param_cols
        if pd.notnull(row[column])
    }


def preprocess_order(
    exchange: ccxt.Exchange,
    symbol: str,
    order_type: str,
    amount: float,
    price: float,
    cost: float,
    markets: pd.DataFrame,
    max_cost: float,
    cost_out_of_range: Literal["warn", "clip"] = "warn",
    price_out_of_range: Literal["warn", "clip"] = "warn",
    amount_out_of_range: Literal["warn", "clip"] = "warn",
) -> tuple:
    market = markets[markets["symbol"] == symbol].reindex(columns=order_data_columns)
    if market.empty:
        raise ValueError(f"Symbol '{symbol}' not found in markets")
    market[cap_zero_columns] = market[cap_zero_columns].fillna(0)
    market[cap_inf_columns] = market[cap_inf_columns].fillna(np.inf)
    market = market.to_dict("records")[0]
    if pd.isnull(amount) and (pd.notnull(cost) and pd.notnull(price)):
        amount = cost / price
    elif pd.isnull(cost) and (pd.notnull(amount) and pd.notnull(price)):
        cost = amount * price
    if (order_type == "limit") and pd.isnull(price):
        raise ValueError("Missing price for limit order.")
    if pd.notnull(cost):
        if cost > max_cost:
            raise ValueError(f"Order cost {cost} larger than limit {max_cost}")
    values = {"amount": amount, "price": price, "cost": cost}
    new_values = {}
    for key, value in values.items():
        if pd.isnull(value):
            new_values[key] = value
            continue
        if key == "price":
            out_of_range = price_out_of_range
        elif key == "cost":
            out_of_range = cost_out_of_range
        else:
            out_of_range = amount_out_of_range
        limits_min = market[f"limits_{key}.min"]
        limits_max = market[f"limits_{key}.max"]
        if out_of_range == "warn":
            if not limits_min <= value <= limits_max:
                warnings.warn(
                    f"{key} {value} for {symbol} outside limits {limits_min}, {limits_max}."
                )
                value = None
        else:
            value = np.clip(value, limits_min, limits_max)
        new_values[key] = value
    new_values["amount"] = exchange.amount_to_precision(
        symbol=symbol, amount=new_values["amount"]
    )
    new_values["price"] = exchange.price_to_precision(
        symbol=symbol, price=new_values["price"]
    )
    return new_values["amount"], new_values["price"]


def check_orders_dataframe_size(
    orders: pd.DataFrame, max_number_of_orders: int = 5
) -> None:
    n_orders = len(orders.index)
    if n_orders > max_number_of_orders:
        raise ValueError(
            f"Number of orders {n_orders} larger than limit {max_number_of_orders}"
        )


def preprocess_order_dataframe(
    orders: pd.DataFrame,
    markets: pd.DataFrame,
    max_orders: int,
    max_cost: float,
    cost_out_of_range: Literal["warn", "clip"] = "warn",
    price_out_of_range: Literal["warn", "clip"] = "warn",
    amount_out_of_range: Literal["warn", "clip"] = "warn",
) -> pd.DataFrame:
    check_orders_dataframe_size(orders=orders, max_number_of_orders=max_orders)
    orders = date_time_columns_to_int_str(orders)
    if {"amount", "price"}.issubset(orders.columns):
        orders["cost"] = orders["amount"] * orders["price"]
    elif {"cost", "price"}.issubset(orders.columns):
        orders["amount"] = orders["cost"] / orders["price"]
    if "cost" in orders.columns:
        orders_error = orders[orders["cost"] > max_cost]
        if not orders_error.empty:
            raise ValueError(f"Orders exceeding max cost: {orders_error}")
    order_markets = markets.reindex(columns=order_data_columns)
    order_markets[cap_zero_columns] = order_markets[cap_zero_columns].fillna(0)
    order_markets[cap_inf_columns] = order_markets[cap_inf_columns].fillna(np.inf)
    orders = orders.merge(order_markets)
    for column, out_of_range in [
        ("cost", cost_out_of_range),
        ("price", price_out_of_range),
        ("amount", amount_out_of_range),
    ]:
        min_limit, max_limit = f"limits_{column}.min", f"limits_{column}.max"
        if column in orders.columns:
            if out_of_range == "warn":
                in_bounds = orders[column].between(orders[min_limit], orders[max_limit])
                out_of_bounds_orders = orders.loc[~in_bounds].reset_index(drop=True)
                orders = orders.loc[in_bounds].reset_index(drop=True)
                if not out_of_bounds_orders.empty:
                    warnings.warn(
                        f"Removing orders with {column} outside limits:\n{out_of_bounds_orders.to_markdown(index=False)}"
                    )
            else:
                orders[column] = orders[column].clip(
                    orders[min_limit], orders[max_limit]
                )
    if "params" not in orders.columns:
        param_cols = orders.columns[orders.columns.str.startswith("params.")]
        orders["params"] = orders.apply(combine_params, axis=1, param_cols=param_cols)
    return orders


@overload
def concat_results(
    results: list[pd.DataFrame],
    errors: Literal["raise", "warn", "ignore"] = "raise",
) -> DataFrame: ...


@overload
def concat_results(
    results: list[dict],
    errors: Literal["raise", "warn", "ignore"] = "raise",
) -> DataFrame: ...


@overload
def concat_results(
    results: list[None],
    errors: Literal["raise", "warn", "ignore"] = "raise",
) -> list[None]: ...


def concat_results(
    results: list[pd.DataFrame | dict | None],
    errors: Literal["raise", "warn", "ignore"] = "raise",
) -> DataFrame | list[dict | DataFrame | None]:
    """Concatenate results from asyncio gather"""
    clean_results, errors_results = [], []
    for x in results:
        if isinstance(x, dict):
            clean_results.append(x)
        elif isinstance(x, pd.DataFrame):
            clean_results.append(x)
        else:
            errors_results.append(x)
    if errors_results:
        if errors == "raise":
            raise ValueError(f"Errors encountered: {errors_results}")
        elif errors == "warn":
            warnings.warn(f"Errors encountered: {errors_results}")
    if clean_results:
        if all([isinstance(x, pd.DataFrame) for x in clean_results]):
            return pd.concat(clean_results, ignore_index=True)
        elif all([isinstance(x, dict) for x in clean_results]):
            return pd.DataFrame(data=clean_results).drop(
                columns=["info"], errors="ignore"
            )
        else:
            return clean_results
    else:
        return pd.DataFrame()


async def async_concat_results(
    tasks: Awaitable | list[Awaitable] | list[list[Awaitable]],
    errors: Literal["raise", "warn", "ignore"] = "raise",
) -> DataFrame | list[DataFrame] | Any:
    # Single coroutine
    if isinstance(tasks, Awaitable):
        return await tasks
    # Flat list of awaitables
    elif all(isinstance(t, Awaitable) for t in tasks):
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return concat_results(results=results, errors=errors)
    elif all(
        isinstance(group, list) and all(isinstance(t, Awaitable) for t in group)
        for group in tasks
    ):
        flat_tasks = [t for group in tasks for t in group]
        flat_results = await asyncio.gather(*flat_tasks, return_exceptions=True)
        # Reconstruct shape
        results = []
        i = 0
        for group in tasks:
            group_size = len(group)
            group_results = flat_results[i : i + group_size]
            group_results = concat_results(results=group_results, errors=errors)
            results.append(group_results)
            i += group_size
        return results
    else:
        raise TypeError(
            "Expected coroutine, list of coroutines, or list of lists of coroutines."
        )


def filter_empty_data(data: Union[dict, pd.DataFrame]) -> Union[dict, pd.DataFrame]:
    if isinstance(data, pd.DataFrame):
        data = data.dropna(axis=1, how="all", ignore_index=True)
    return data


def append_non_empty(
    results: list,
    data: Union[dict, pd.DataFrame],
) -> list:
    data = filter_empty_data(data=data)
    if data is not None:
        results.append(data.copy())
    return results


def format_from_to_timestamp(
    timestamp: int | pd.Timestamp | dict | str | None,
) -> pd.Timestamp:
    now = pd.Timestamp.now(tz="UTC")
    if isinstance(timestamp, dict):
        timestamp = now + pd.DateOffset(**timestamp)
    elif isinstance(timestamp, str):
        timestamp = now + pd.Timedelta(timestamp)
    elif isinstance(timestamp, (pd.Timedelta, np.timedelta64)):
        timestamp += now
    elif timestamp is None:
        timestamp = now
    return timestamp


def drop_duplicates(
    data: pd.DataFrame, from_date: pd.Timestamp, to_date: pd.Timestamp
) -> pd.DataFrame:
    duplicate_columns = ["timestamp"]
    if "id" in data.columns:
        duplicate_columns.append("id")
    if "symbol" in data.columns:
        duplicate_columns.append("symbol")
    return data.loc[data["timestamp"].between(from_date, to_date)].drop_duplicates(
        subset=duplicate_columns, ignore_index=True, keep="last"
    )


def merge_markets_with_balances(
    markets: pd.DataFrame, balance: pd.DataFrame
) -> pd.DataFrame:
    balance = balance.drop(columns=["datetime", "timestamp"], errors="ignore")
    if "base_free" in balance.columns:
        markets = markets.merge(balance)
    else:
        for column in ["base", "quote", "settle"]:
            column_renaming = {
                x: f"{column}_{x}" for x in ["free", "used", "total", "debt"]
            }
            markets = markets.merge(
                balance.rename(columns={"symbol": column}), how="left"
            ).rename(columns=column_renaming)
    return markets


@dataclass
class FunctionHandler:
    errors: Literal["raise", "warn", "ignore"] = "raise"

    def try_function(
        self,
        function: Callable[..., Union[pd.DataFrame, dict, None]],
        **kwargs: dict,
    ) -> pd.DataFrame | dict | None:
        try:
            return function(**kwargs)
        except Exception as e:
            if self.errors == "ignore":
                return None
            elif self.errors == "warn":
                warnings.warn(f"{function}({kwargs}): {e}")
                return None
            else:
                raise ValueError(f"{function}({kwargs}): {e}") from e

    def load_full_dataset(
        self,
        function: Callable[..., pd.DataFrame],
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        time_increment: str = "7d",
        limit: int = 1000,
        **kwargs: Any,
    ) -> pd.DataFrame:
        from_date = format_from_to_timestamp(from_date)
        to_date = format_from_to_timestamp(to_date)
        since = from_date
        length_data = limit
        df = []
        kwargs["limit"] = limit
        if from_date:
            while (length_data == limit) and (since < to_date):
                kwargs.update(since=since)
                data = self.try_function(function=function, **kwargs)
                if data is not None and len(data) > 0:
                    df.append(data.copy())
                    since = data["timestamp"].max()
                else:
                    length_data = limit
                    since = min(since + pd.Timedelta(time_increment), to_date)
            if df:
                return drop_duplicates(
                    data=pd.concat(df), from_date=from_date, to_date=to_date
                )
            else:
                return pd.DataFrame()
        else:
            return self.try_function(function=function, **kwargs)

    def load_dataset_into_cache(
        self,
        data: pd.DataFrame,
        function: Callable[..., pd.DataFrame],
        from_date: pd.Timestamp | dict | str,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int = 1000,
        **kwargs: Any,
    ) -> pd.DataFrame:
        from_date = format_from_to_timestamp(from_date)
        to_date = format_from_to_timestamp(to_date)
        since = from_date if data.empty else data["timestamp"].max()
        new_data = self.load_full_dataset(
            function=function,
            from_date=since,
            to_date=to_date,
            limit=limit,
            **kwargs,
        )
        if not new_data.empty:
            data = pd.concat([data, new_data])
        if not data.empty:
            data = drop_duplicates(data=data, from_date=from_date, to_date=to_date)
        return data

    def load_multi_symbol_dataset(
        self,
        function: Callable[..., Union[pd.DataFrame, dict]],
        symbols: list[str],
        symbol_column: Literal["symbol", "code"] = "symbol",
        **kwargs: Any,
    ) -> pd.DataFrame:
        df = []
        for symbol in symbols:
            kwargs[symbol_column] = symbol
            data = self.try_function(function=function, **kwargs)
            if isinstance(data, (dict, pd.DataFrame)) and len(data):
                data[symbol_column] = symbol
                df.append(data.copy())
        return concat_results(df)

    def load_full_multi_symbol_dataset(
        self,
        function: Callable[..., pd.DataFrame],
        symbols: list[str],
        symbol_column: Literal["symbol", "code"] = "symbol",
        from_date: pd.Timestamp | dict | str | None = None,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int = 1000,
        time_increment: str = "7d",
        **kwargs: Any,
    ) -> pd.DataFrame:
        results = []
        for symbol in symbols:
            df = self.load_full_dataset(
                function=function,
                from_date=from_date,
                to_date=to_date,
                time_increment=time_increment,
                limit=limit,
                symbol=symbol,
                **kwargs,
            )
            if not df.empty:
                df[symbol_column] = symbol
                results.append(df.copy())
        return concat_results(results)

    def load_multi_symbol_dataset_into_cache(
        self,
        function: Callable[..., pd.DataFrame],
        data: pd.DataFrame,
        symbols: list[str],
        from_date: pd.Timestamp | dict | str,
        to_date: pd.Timestamp | dict | str | None = None,
        limit: int = 1000,
        symbol_column: str = "symbol",
        **kwargs: Any,
    ) -> pd.DataFrame:
        results = []
        for symbol in symbols:
            subset = (
                data[data[symbol_column] == symbol] if not data.empty else data.copy()
            )
            updated = self.load_dataset_into_cache(
                data=subset,
                function=function,
                from_date=from_date,
                to_date=to_date,
                limit=limit,
                symbol=symbol,
                **kwargs,
            )
            if not updated.empty:
                updated[symbol_column] = symbol
                results.append(updated.copy())
        return concat_results(results)

    def loop_through_orders_in_chunks(
        self,
        function: Callable[..., pd.DataFrame],
        orders: pd.DataFrame,
        chunk_size: int = 5,
        max_number_of_orders: int = 5,
        **kwargs: Any,
    ) -> pd.DataFrame:
        check_orders_dataframe_size(orders, max_number_of_orders)
        results = []
        while not orders.empty:
            result = self.try_function(
                function=function,
                orders=orders.head(chunk_size).reset_index(drop=True),
                **kwargs,
            )
            orders = orders.tail(-chunk_size).reset_index(drop=True)
            results.append(result)
        return concat_results(results)

    def loop_through_orders(
        self,
        function: Callable[..., pd.DataFrame],
        orders: pd.DataFrame,
        max_number_of_orders: int = 5,
        **kwargs: Any,
    ) -> pd.DataFrame:
        check_orders_dataframe_size(orders, max_number_of_orders)
        results = []
        for order in orders.to_dict(orient="records"):
            full_args = {**order, **kwargs}
            result = self.try_function(function=function, **full_args)
            results.append(result)
        return concat_results(results)

    def call_per_group_concat(
        self,
        function: Callable[..., pd.DataFrame],
        orders: pd.DataFrame,
        group_col: str = "symbol",
        id_col: str = "id",
        **kwargs: Any,
    ) -> pd.DataFrame:
        results = []
        for key, grp in orders.groupby(group_col):
            result = self.try_function(
                function=function,
                **{group_col: key, f"{id_col}s": grp[id_col].tolist(), **kwargs},
            )
            if not result.empty:
                results.append(result.copy())
        return concat_results(results)


def create_full_async_tasks(
    function: Callable,
    from_date: pd.Timestamp | dict | str | None = None,
    to_date: pd.Timestamp | dict | str | None = None,
    timeframe: str = "1m",
    limit: int = 1000,
    **kwargs: Any,
) -> list[Awaitable[dict | pd.DataFrame]]:
    tasks = []
    pandas_timeframe = timeframe if timeframe != "1m" else "1min"
    pandas_timeframe = pd.Timedelta(pandas_timeframe)
    pandas_timeframe_limit = limit * pandas_timeframe
    from_date = format_from_to_timestamp(from_date)
    to_date = format_from_to_timestamp(to_date)
    start_times = pd.date_range(
        start=from_date, end=to_date, freq=pandas_timeframe_limit, inclusive="left"
    ).tolist()
    if start_times:
        for since in start_times:
            end_time = min(since + pandas_timeframe_limit, to_date)
            task_kwargs = {
                **kwargs,
                "timeframe": timeframe,
                "since": since,
                "limit": int((end_time - since) / pandas_timeframe),
            }
            tasks.append(function(**task_kwargs))
    else:
        task_kwargs = {
            **kwargs,
            "limit": limit,
            "timeframe": timeframe,
        }
        tasks.append(function(**task_kwargs))
    return tasks


def create_multi_symbol_async_tasks(
    function: Callable,
    symbols: list[str],
    symbol_column: Literal["symbol", "code"] = "symbol",
    **kwargs: Any,
) -> list[Awaitable[dict | pd.DataFrame]]:
    tasks = []
    for symbol in symbols:
        tasks.append(function(**{**kwargs, symbol_column: symbol}))
    return tasks


def create_full_multi_symbol_async_tasks(
    function: Callable[..., pd.DataFrame],
    symbols: list[str],
    symbol_column: Literal["symbol", "code"] = "symbol",
    from_date: pd.Timestamp | dict | str | None = None,
    to_date: pd.Timestamp | dict | str | None = None,
    timeframe: str = "1m",
    limit: int = 1000,
    **kwargs: Any,
) -> list[Awaitable[dict | pd.DataFrame]]:
    tasks = []
    for symbol in symbols:
        symbol_tasks = create_full_async_tasks(
            function=function,
            from_date=from_date,
            to_date=to_date,
            timeframe=timeframe,
            limit=limit,
            **{**kwargs, symbol_column: symbol},
        )
        tasks += symbol_tasks
    return tasks


def async_loop_through_orders(
    function: Callable[..., Awaitable[pd.DataFrame]],
    orders: pd.DataFrame,
    max_number_of_orders: int = 5,
    **kwargs: Any,
) -> list[Awaitable[dict | pd.DataFrame]]:
    check_orders_dataframe_size(orders, max_number_of_orders)
    tasks = []
    for order in orders.to_dict(orient="records"):
        full_args = {**order, **kwargs}
        tasks.append(function(**full_args))
    return tasks


def async_loop_through_orders_in_chunks(
    function: Callable[..., Awaitable[pd.DataFrame]],
    orders: pd.DataFrame,
    max_number_of_orders: int = 5,
    chunk_size: int = 5,
    **kwargs: Any,
) -> list[Awaitable[dict | pd.DataFrame]]:
    check_orders_dataframe_size(orders, max_number_of_orders)
    tasks = []
    orders_copy = orders.copy()
    while not orders_copy.empty:
        tasks.append(
            function(
                orders=orders_copy.head(chunk_size).reset_index(drop=True),
                **kwargs,
            )
        )
        orders_copy = orders_copy.tail(-chunk_size).reset_index(drop=True)
    return tasks


def async_call_per_group_concat(
    function: Callable[..., Awaitable[pd.DataFrame]],
    orders: pd.DataFrame,
    group_col: str = "symbol",
    id_col: str = "id",
    **kwargs: Any,
) -> list[Awaitable[pd.DataFrame]]:
    tasks = []
    for key, grp in orders.groupby(group_col):
        tasks.append(
            function(**{group_col: key, f"{id_col}s": grp[id_col].tolist(), **kwargs})
        )
    return tasks
