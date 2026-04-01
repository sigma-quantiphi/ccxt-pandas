"""Fetch and analyze open interest history.

Fetches open interest history for BTC/USDT:USDT from Binance
and calculates percentage changes.
No API keys required — uses public market data.
"""

import ccxt

from ccxt_pandas import CCXTPandasExchange

exchange = ccxt.binance()
exchange = CCXTPandasExchange(exchange=exchange)
open_interest = exchange.fetch_open_interest_history(symbol="BTC/USDT:USDT")
open_interest["pct_change"] = open_interest["openInterestAmount"].pct_change()
print(open_interest)
