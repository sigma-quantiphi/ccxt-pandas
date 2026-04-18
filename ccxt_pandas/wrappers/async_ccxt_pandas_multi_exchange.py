from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

import ccxt.pro as ccxt_pro

from ccxt_pandas.wrappers.async_ccxt_pandas_exchange import AsyncCCXTPandasExchange


@dataclass
class AsyncCCXTPandasMultiExchange:
    """
    Manages multiple CCXT Pro-based asynchronous exchanges, returning task lists
    for unified concurrent execution across exchanges.

    Attributes:
        exchange_names (tuple): Exchange identifiers to initialize.
        exchanges (dict[str, AsyncCCXTPandasExchange]): Exchange ID → async client mapping.
    """

    exchange_names: tuple = ()
    exchanges: dict[str, AsyncCCXTPandasExchange] | None = None

    def __post_init__(self):
        if self.exchanges is None:
            self.exchanges = {}
            for exchange_id in self.exchange_names:
                exchange_class = getattr(ccxt_pro, exchange_id)
                exchange = exchange_class()
                self.exchanges[exchange_id] = AsyncCCXTPandasExchange(
                    exchange=exchange, exchange_name=exchange_id
                )

    def __getattr__(self, method_name) -> Callable[[tuple[Any, ...], dict[str, Any]], list]:
        def wrapper_function(*args, **kwargs) -> list:
            tasks = []
            for name, exchange in self.exchanges.items():
                method = getattr(exchange, method_name)
                task = method(*args, **kwargs)
                if isinstance(task, list):
                    tasks += task
                else:
                    tasks.append(task)
            return tasks

        return wrapper_function

    def close(self) -> list:
        return [exchange.close() for exchange in self.exchanges.values()]
