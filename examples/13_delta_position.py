"""Calculate net delta exposure across spot and derivatives.

Fetches balance and positions from OKX sandbox, then computes
the net delta per base asset.
Requires OKX_SANDBOX_API_KEY, OKX_SANDBOX_API_SECRET, OKX_SANDBOX_API_PASSWORD in .env.
"""

import os

import ccxt
import pandas as pd
from dotenv import load_dotenv

from ccxt_pandas import CCXTPandasExchange

load_dotenv()

exchange = ccxt.okx(
    {
        "apiKey": os.environ["OKX_SANDBOX_API_KEY"],
        "secret": os.environ["OKX_SANDBOX_API_SECRET"],
        "password": os.environ["OKX_SANDBOX_API_PASSWORD"],
    }
)
exchange.set_sandbox_mode(True)
pandas_exchange = CCXTPandasExchange(exchange=exchange)

markets = pandas_exchange.load_markets()
balance = pandas_exchange.fetch_balance()
positions = pandas_exchange.fetch_positions()

# Rename symbol to base
balance = balance.rename(columns={"symbol": "base", "free": "amount"})
print(balance.to_markdown(index=False))

# Merge markets onto positions
positions = positions.merge(markets[["symbol", "base"]])
positions["amount"] = positions["contracts"].where(
    positions["side"] == "long", other=-positions["contracts"]
)
positions["amount"] *= positions["contractSize"]
print(positions.to_markdown(index=False))

# Concat and sum by base
delta = (
    pd.concat([balance, positions], ignore_index=True)
    .groupby("base", as_index=False)["amount"]
    .sum()
)
print(delta.to_markdown(index=False))
