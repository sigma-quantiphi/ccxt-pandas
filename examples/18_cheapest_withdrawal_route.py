"""Find the cheapest cross-exchange withdrawal route per currency.

Concatenates `fetch_currencies` from binance / bybit / okx, joins withdrawals
against deposits on `(currency_id, network)`, drops same-exchange routes, and
sorts the remaining routes by withdrawal fee. Useful when you need to move a
balance between venues and want to pick the cheapest rail.

Requires demo API keys for each exchange in .env:
  BINANCE_DEMO_API_KEY / BINANCE_DEMO_API_SECRET
  BYBIT_DEMO_API_KEY / BYBIT_DEMO_API_SECRET
  OKX_DEMO_API_KEY / OKX_DEMO_API_SECRET / OKX_DEMO_API_PASSWORD
"""

import os

import ccxt
import pandas as pd
from dotenv import load_dotenv

from ccxt_pandas import CCXTPandasExchange

load_dotenv()

binance = CCXTPandasExchange(
    exchange=ccxt.binance(
        {
            "apiKey": os.getenv("BINANCE_DEMO_API_KEY"),
            "secret": os.getenv("BINANCE_DEMO_API_SECRET"),
        }
    )
)
bybit = CCXTPandasExchange(
    exchange=ccxt.bybit(
        {
            "apiKey": os.getenv("BYBIT_DEMO_API_KEY"),
            "secret": os.getenv("BYBIT_DEMO_API_SECRET"),
        }
    )
)
okx = CCXTPandasExchange(
    exchange=ccxt.okx(
        {
            "apiKey": os.getenv("OKX_DEMO_API_KEY"),
            "secret": os.getenv("OKX_DEMO_API_SECRET"),
            "password": os.getenv("OKX_DEMO_API_PASSWORD"),
        }
    )
)

currencies = pd.concat(
    [binance.fetch_currencies(), bybit.fetch_currencies(), okx.fetch_currencies()],
    ignore_index=True,
)

withdrawals = currencies.query("withdraw == True")[
    ["id", "code", "network_id", "network", "network_fee", "exchange"]
]
deposits = currencies.query("deposit == True")[["id", "code", "network_id", "network", "exchange"]]

routes = (
    withdrawals.merge(deposits, on=["id", "network"], suffixes=("_withdraw", "_deposit"))
    .query("exchange_withdraw != exchange_deposit")
    .sort_values(["id", "network_fee", "exchange_withdraw", "exchange_deposit"])
)

# Cheapest rail per (currency, network):
cheapest = routes.loc[
    routes.groupby(["id", "network"])["network_fee"].idxmin().dropna()
].reset_index(drop=True)

print("All cross-exchange routes (head):")
print(routes.head(20).to_markdown(index=False))
print("\nCheapest rail per (currency, network):")
print(cheapest.head(20).to_markdown(index=False))
