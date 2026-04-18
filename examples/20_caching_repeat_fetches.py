"""Demonstrate the `cache=True` parameter on fetch_trades.

When `cache=True`, repeated calls with the same `(symbol, from_date)` reuse
prior pages and only fetch new trades since the last call. Latency drops
sharply after the first call.

No API keys required — uses public market data.
"""

import time

import ccxt
import pandas as pd

from ccxt_pandas import CCXTPandasExchange

exchange = ccxt.binance()
pandas_exchange = CCXTPandasExchange(exchange=exchange)
from_date = pd.Timestamp.utcnow() - pd.Timedelta(minutes=5)

for i in range(5):
    t0 = time.perf_counter()
    trades = pandas_exchange.fetch_trades(symbol="BTC/USDT", from_date=from_date, cache=True)
    dt = time.perf_counter() - t0
    print(f"Call {i + 1}: {dt:.3f}s — {len(trades):,} trades")
