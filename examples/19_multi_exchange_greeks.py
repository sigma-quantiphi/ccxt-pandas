"""Aggregate option Greeks across binance, bybit, and okx into one DataFrame.

Each exchange exposes `fetch_all_greeks` differently — okx requires a `uly`
filter for the underlying. This concatenates them all so you can scan
Greeks across venues from a single frame.

No API keys required — uses public market data.
"""

import ccxt
import pandas as pd

from ccxt_pandas import CCXTPandasExchange

frames = []
for exchange_id in ["binance", "bybit", "okx"]:
    exchange = getattr(ccxt, exchange_id)(
        {"options": {"loadAllOptions": True, "defaultType": "option"}}
    )
    pandas_exchange = CCXTPandasExchange(exchange=exchange)
    params = {"uly": "BTC-USD"} if exchange_id == "okx" else {}
    greeks = pandas_exchange.fetch_all_greeks(params=params)
    frames.append(greeks)

greeks = pd.concat(frames, ignore_index=True)
print(greeks.tail(20).to_markdown(index=False))
print(f"\nTotal contracts: {len(greeks)} across {greeks['exchange'].nunique()} exchanges")
