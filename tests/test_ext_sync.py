import os
import time

import ccxt
import pandas as pd
from dotenv import load_dotenv

from ccxt_pandas import CCXTPandasExchange

load_dotenv()
exchange = ccxt.binance(
    {
        "apiKey": os.getenv("SANDBOX_API_KEY"),
        "secret": os.getenv("SANDBOX_API_SECRET"),
    }
)
exchange.enable_demo_trading(True)
pandas_exchange = CCXTPandasExchange(
    exchange=exchange,
    max_number_of_orders=100,
)

# Define parameters
now = pd.Timestamp.now(tz="UTC")
end_date = now.floor("1min")
start_date = end_date - pd.Timedelta(minutes=2)
symbols = ["BTC/USDT", "BNB/USDT", "XRP/USDT", "DOGE/USDT"]
trades = pandas_exchange.fetch_trades(
    symbol=symbols[0], from_date=start_date, to_date=end_date, limit=500
)
end_date = now.floor("1d")
start_date = end_date - pd.Timedelta(days=5)
ohlcv = pandas_exchange.fetch_ohlcv(symbol=symbols[0], from_date=start_date, timeframe="1m")
start_date = end_date - pd.Timedelta(days=100)
my_trades = pandas_exchange.fetch_my_trades(
    symbol=symbols, from_date=start_date, to_date=end_date
)
print(my_trades)

for i in range(5):
    start_time = time.time()
    end_date = pd.Timestamp.now(tz="UTC")
    start_date = end_date - pd.Timedelta(minutes=10)
    trades = pandas_exchange.fetch_trades(
        symbol=symbols, from_date=start_date, to_date=end_date, cache=True
    )
    elapsed_time = time.time() - start_time
    print(f"Run {i + 1} - Execution time: {elapsed_time:.2f} seconds")
    print(trades)

trades = trades.drop_duplicates(subset=["symbol"], keep="last")[["symbol", "price"]]
trades["price"] /= 2
trades["side"] = "buy"
trades["notional"] = 12
trades["type"] = "limit"
trades = trades.loc[trades.index.repeat(3)].reset_index(drop=True)
# Single order methods
response = pandas_exchange.create_order_from_dataframe(orders=trades)
print(response)
orders = pandas_exchange.fetch_open_orders(symbol=symbols)[
    ["id", "price", "amount", "side", "type", "symbol"]
]
print(orders)
orders["price"] *= 1.1
orders = pandas_exchange.edit_order_from_dataframe(
    orders=orders,
)
print(orders)
cancel_response = pandas_exchange.cancel_order_from_dataframe(
    orders=orders[["id", "symbol"]]
)
print(cancel_response)

# Multi order endpoints
orders = pandas_exchange.create_orders_from_dataframe(
    orders=trades,
)
print(orders)
orders = pandas_exchange.fetch_open_orders(symbol=symbols)[
    ["id", "price", "amount", "side", "type", "symbol"]
]
print(orders)
orders["price"] *= 1.1
orders = pandas_exchange.edit_orders_from_dataframe(orders=orders)
print(orders)
cancel_response = pandas_exchange.cancel_orders_from_dataframe(
    orders=orders[["id", "symbol"]]
)
print(cancel_response)

# Cancel all orders
orders = pandas_exchange.create_orders_from_dataframe(
    orders=orders,
)
print(orders)
cancel_response = pandas_exchange.cancel_all_orders(
    symbol=symbols,
)
print(cancel_response)
