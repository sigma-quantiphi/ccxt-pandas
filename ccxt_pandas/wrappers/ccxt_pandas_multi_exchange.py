from dataclasses import dataclass
from typing import Callable, Literal

import ccxt
import pandas as pd

from ccxt_pandas.wrappers.ccxt_pandas_exchange import CCXTPandasExchange
from ccxt_pandas.utils.pandas_utils import concat_results, append_non_empty


@dataclass
class CCXTPandasMultiExchange:
    """
    Manages multiple cryptocurrency exchanges and aggregates method call
    results into unified DataFrames.

    Attributes:
        exchange_names (tuple): Exchange identifiers to initialize.
        exchanges (dict[str, CCXTPandasExchange]): Exchange ID → client mapping.
        errors (str): Error handling mode: "raise", "warn", or "ignore".
    """

    exchange_names: tuple = ()
    exchanges: dict[str, CCXTPandasExchange] | None = None
    errors: Literal["ignore", "raise", "warn"] = "raise"

    def __post_init__(self):
        if self.exchanges is None:
            self.exchanges = {}
            for exchange_id in self.exchange_names:
                exchange_class = getattr(ccxt, exchange_id)
                exchange = exchange_class()
                self.exchanges[exchange_id] = CCXTPandasExchange(
                    exchange=exchange, exchange_name=exchange_id, errors=self.errors
                )

    def __getattr__(self, method_name) -> Callable[..., pd.DataFrame]:
        def wrapper_function(*args, **kwargs) -> pd.DataFrame:
            results = []
            for name, exchange in self.exchanges.items():
                method = getattr(exchange, method_name)
                data = method(*args, **kwargs)
                results = append_non_empty(results=results, data=data)
            return concat_results(results=results)

        return wrapper_function
