from dataclasses import dataclass
from typing import Callable, Any

import ccxt.pro as ccxt
import pandas as pd
from pandas import DataFrame

from ccxt_pandas.wrappers.async_ccxt_pandas_exchange import AsyncCCXTPandasExchange
from ccxt_pandas.wrappers.method_mappings import orders_methods
from ccxt_pandas.wrappers.models import ExchangeClientConfig


@dataclass
class AsyncCCXTPandasMultiAccount:
    """
    Manages multiple asynchronous CCXT exchange clients, enabling unified
    multi-account operations that return task lists for concurrent execution.

    Attributes:
        accounts (dict[str, ExchangeClientConfig]): Account name → config mapping.
        clients (dict[str, AsyncCCXTPandasExchange]): Account name → async client mapping.
    """

    accounts: dict[str, ExchangeClientConfig] = None
    clients: dict[str, AsyncCCXTPandasExchange] = None

    def __post_init__(self):
        if self.clients is None:
            self.clients = {}
            for account_name, account in self.accounts.items():
                exchange_class = getattr(ccxt, account["exchange"])
                exchange = exchange_class(
                    {
                        k: v
                        for k, v in account.items()
                        if k not in ["account", "exchange", "sandboxMode"]
                    }
                )
                exchange.set_sandbox_mode(account["sandboxMode"])
                self.clients[account_name] = AsyncCCXTPandasExchange(
                    exchange=exchange,
                    exchange_name=exchange.id,
                    account_name=account_name,
                )

    def __getattr__(
        self, method_name: str
    ) -> Callable[[tuple[Any, ...], dict[str, Any]], list[Callable[..., DataFrame]]]:
        def wrapper(*args, **kwargs) -> list[Callable[..., pd.DataFrame]]:
            tasks = []
            if method_name in orders_methods:
                orders = kwargs.pop("orders")
                for account, account_orders in orders.groupby("account"):
                    client = self.clients[account]
                    method = getattr(client, method_name)
                    tasks_kwargs = {
                        **kwargs,
                        "orders": account_orders.drop(
                            columns=["account", "exchange"], errors="ignore"
                        ),
                    }
                    task = method(*args, **tasks_kwargs)
                    if isinstance(task, list):
                        tasks += task
                    else:
                        tasks.append(task)
            else:
                for account, client in self.clients.items():
                    method = getattr(client, method_name)
                    task = method(*args, **kwargs)
                    if isinstance(task, list):
                        tasks += task
                    else:
                        tasks.append(task)
            return tasks

        return wrapper

    def close(self) -> list:
        return [client.close() for client in self.clients.values()]
