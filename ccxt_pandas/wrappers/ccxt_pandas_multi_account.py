from dataclasses import dataclass
from typing import Callable, Literal

import ccxt
import pandas as pd

from ccxt_pandas.wrappers.ccxt_pandas_exchange import CCXTPandasExchange
from ccxt_pandas.wrappers.method_mappings import orders_methods
from ccxt_pandas.wrappers.models import ExchangeClientConfig
from ccxt_pandas.utils.pandas_utils import concat_results, append_non_empty


@dataclass
class CCXTPandasMultiAccount:
    """
    Manages multiple CCXT accounts and delegates method calls to each,
    aggregating results into unified DataFrames.

    Attributes:
        accounts (dict[str, ExchangeClientConfig]): Account name → config mapping.
        clients (dict[str, CCXTPandasExchange]): Account name → exchange client mapping.
        errors (str): Error handling mode: "raise", "warn", or "ignore".
    """

    accounts: dict[str, ExchangeClientConfig] = None
    clients: dict[str, CCXTPandasExchange] = None
    errors: Literal["ignore", "raise", "warn"] = "raise"

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
                self.clients[account_name] = CCXTPandasExchange(
                    exchange=exchange,
                    exchange_name=exchange.id,
                    account_name=account_name,
                    errors=self.errors,
                )

    def __getattr__(self, method_name: str) -> Callable[..., pd.DataFrame]:
        def wrapper(*args, **kwargs) -> pd.DataFrame:
            results = []
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
                    data = method(*args, **tasks_kwargs)
                    results = append_non_empty(results=results, data=data)
            else:
                for account, client in self.clients.items():
                    method = getattr(client, method_name)
                    data = method(*args, **kwargs)
                    results = append_non_empty(results=results, data=data)
            return concat_results(results=results)

        return wrapper
