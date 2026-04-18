"""Synchronous basics: market data, orders, and account queries.

Demonstrates CCXTPandasExchange with Binance sandbox — fetching OHLCV,
order books, trades, funding rates, and creating/editing/cancelling orders.

Requires SANDBOX_API_KEY and SANDBOX_API_SECRET in .env file.
"""

import os

import ccxt
import pandas as pd
from dotenv import load_dotenv

from ccxt_pandas import CCXTPandasExchange

load_dotenv()

# --- Initialize exchange ---
exchange = ccxt.binance(
    {
        "apiKey": os.getenv("SANDBOX_API_KEY"),
        "secret": os.getenv("SANDBOX_API_SECRET"),
    }
)
exchange.set_sandbox_mode(True)
pandas_exchange = CCXTPandasExchange(exchange=exchange)
symbol = "BNB/USDT:USDT"

# --- Market data ---

# Load available symbols
symbols = pandas_exchange.load_markets()
print(symbols)

# Fetch OHLCV
ohlcv = pandas_exchange.fetch_ohlcv(symbol=symbol, timeframe="1m", limit=1000)
print(ohlcv.tail().to_markdown(index=False))

# Fetch Order Book
order_book = pandas_exchange.fetch_order_book(symbol=symbol, limit=1000)
print(order_book.tail().to_markdown(index=False))

# Fetch Bids & Asks (All Symbols)
bids_asks = pandas_exchange.fetch_bids_asks()
print(bids_asks.tail().to_markdown(index=False))

# Fetch Trades
trades = pandas_exchange.fetch_trades(symbol=symbol, limit=1000)
print(trades.tail().to_markdown(index=False))

# Fetch Current Funding Rates (All Perpetuals)
funding_rates = pandas_exchange.fetch_funding_rates()
print(funding_rates.tail().to_markdown(index=False))

# Fetch Historical Funding Rate
funding_rate_history = pandas_exchange.fetch_funding_rate_history(symbol=symbol, limit=1000)
print(funding_rate_history.tail().to_markdown(index=False))

# --- Orders ---

# Create 4 limit orders: 2 buys and 2 sells at min/max OHLCV prices
orders = pd.DataFrame({"side": ["buy", "buy", "sell", "sell"]})
orders["price"] = [
    ohlcv["low"].min(),
    ohlcv["high"].max(),
    ohlcv["high"].max(),
    ohlcv["high"].min(),
]
orders["symbol"] = symbol
orders["cost"] = 7
orders["type"] = "limit"
print(orders.to_markdown(index=False))

create_response = pandas_exchange.create_orders(orders=orders)
print(create_response.tail().to_markdown(index=False))

# Fetch My Trades
my_trades = pandas_exchange.fetch_my_trades(symbol=symbol, limit=1000)
print(my_trades.tail().to_markdown(index=False))

# Fetch Open Orders
open_orders = pandas_exchange.fetch_open_orders(symbol=symbol)
print(open_orders.tail().to_markdown(index=False))

# Edit Open Orders — double volume, same price
open_orders["amount"] *= 2
edit_response = pandas_exchange.edit_orders(
    orders=open_orders[["id", "side", "price", "amount", "type", "symbol"]]
)
print(edit_response.tail().to_markdown(index=False))

# Cancel All Orders
cancel_response = pandas_exchange.cancel_all_orders(symbol=symbol)
print(cancel_response.tail().to_markdown(index=False))
