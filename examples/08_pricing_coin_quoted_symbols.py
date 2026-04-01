"""Convert coin-quoted pairs to USDT-equivalent prices.

Fetches all spot tickers from Binance, then uses USDT pairs as
intermediaries to price non-USDT-quoted symbols in USDT.
No API keys required — uses public market data.
"""

import ccxt

from ccxt_pandas import CCXTPandasExchange

binance = ccxt.binance()
exchange = CCXTPandasExchange(binance)

# Load spot markets
markets = exchange.load_markets().query("type == 'spot'")
print("Quote currencies:", markets["quote"].unique())

# Fetch tickers
tickers = exchange.fetch_tickers().dropna(subset=["last"])
tickers = tickers[["symbol", "last"]].merge(markets[["symbol", "base", "quote"]])

# Get USDT reference prices
usdt_tickers = tickers.query("quote == 'USDT'")
usdt_tickers = usdt_tickers[["last", "symbol", "base"]].rename(
    columns={"last": "usdt_price", "symbol": "intermediate_symbol", "base": "quote"}
)

# Merge to get USDT prices for coin-quoted pairs
tickers = tickers.merge(usdt_tickers)
tickers["usdt_price"] *= tickers["last"]

print(tickers)
print("\nETH pairs:")
print(tickers.query("base == 'ETH'"))
