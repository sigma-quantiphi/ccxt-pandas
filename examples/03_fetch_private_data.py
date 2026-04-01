"""Fetch private account data: trades, positions, and greeks.

Demonstrates fetching authenticated data from Binance sandbox.
Requires BINANCE_SANDBOX_API_KEY and BINANCE_SANDBOX_API_SECRET in .env.
"""

import os

import ccxt
from dotenv import load_dotenv

from ccxt_pandas import CCXTPandasExchange

load_dotenv()
api_key = os.getenv("BINANCE_SANDBOX_API_KEY")
api_secret = os.getenv("BINANCE_SANDBOX_API_SECRET")

# Initialize exchange (sandbox)
binance = ccxt.binance(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True,
        "options": {"defaultType": "future"},
    }
)
binance.set_sandbox_mode(True)
pandas_exchange = CCXTPandasExchange(exchange=binance)

# === Read trades ===
print("Fetching account trades (sandbox)...")
symbol = "BTC/USDT:USDT"
trades = pandas_exchange.fetch_my_trades(symbol)
print(trades)

# === Read positions ===
print("Fetching positions (sandbox)...")
positions = pandas_exchange.fetch_positions()
print(positions)

# === Fetch greeks (public, no sandbox needed) ===
binance_public = ccxt.binance()
pandas_public = CCXTPandasExchange(exchange=binance_public)
print("Fetching all option Greeks...")
greeks_df = pandas_public.fetch_all_greeks()
print(greeks_df)
