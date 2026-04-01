"""Fetch deposit and withdrawal history.

Demonstrates fetching deposits and withdrawals from Bybit sandbox
with time range filtering.
Requires BYBIT_SANDBOX_API_KEY and BYBIT_SANDBOX_API_SECRET in .env.
"""

import os

import ccxt
import pandas as pd
from dotenv import load_dotenv

from ccxt_pandas import CCXTPandasExchange
from ccxt_pandas.utils.pandas_utils import timestamp_to_int

load_dotenv()
exchange = ccxt.bybit(
    {
        "apiKey": os.getenv("BYBIT_SANDBOX_API_KEY"),
        "secret": os.getenv("BYBIT_SANDBOX_API_SECRET"),
    }
)
exchange.set_sandbox_mode(True)
pandas_exchange = CCXTPandasExchange(exchange=exchange)

start_time = pd.Timestamp("2025-06-21T00:00:00", tz="UTC")
end_time = start_time + pd.Timedelta(days=7)

params = {
    "startTime": timestamp_to_int(start_time),
    "endTime": timestamp_to_int(end_time),
}

deposits = pandas_exchange.fetch_deposits(params=params)
withdrawals = pandas_exchange.fetch_withdrawals(params=params)
data = pd.concat([deposits, withdrawals], ignore_index=True)
print(data)
