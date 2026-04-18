"""Cross-exchange arbitrage detection.

Fetches bids/asks from Binance, Bybit, and KuCoin, then calculates
spread opportunities between different exchanges.
No API keys required — uses public market data.
"""

import ccxt
import pandas as pd

from ccxt_pandas import CCXTPandasExchange

# Setup exchanges
binance = CCXTPandasExchange(exchange=ccxt.binance())
bybit = CCXTPandasExchange(exchange=ccxt.bybit())
kucoin = CCXTPandasExchange(ccxt.kucoinfutures())

# Fetch bids and asks
binance_ba = binance.fetch_bids_asks()
bybit_ba = bybit.fetch_bids_asks()
kucoin_ba = kucoin.fetch_bids_asks()

# Combine
data = pd.concat([binance_ba, bybit_ba, kucoin_ba])
print(data.dropna(axis=1))

# Find all combinations and calculate spread
arbitrage = data[["exchange", "symbol", "bid"]].merge(
    data[["exchange", "symbol", "ask"]], on="symbol", suffixes=("Short", "Long")
)
arbitrage["spread"] = arbitrage["bid"] - arbitrage["ask"]
arbitrage["spreadRelative"] = arbitrage["spread"] / arbitrage[["bid", "ask"]].mean(axis=1)

# Filter for different exchanges for buy/sell
arbitrage = arbitrage.query("exchangeShort != exchangeLong").sort_values(
    "spreadRelative", ascending=False, ignore_index=True
)
print(arbitrage.head(10))
