import os

import pandas as pd
from dotenv import load_dotenv

from ccxt_pandas import CCXTPandasMultiAccount

load_dotenv()

exchange_names = ["binance"]
accounts = {}
for exchange_id in exchange_names:
    key_prefix = "SANDBOX" if exchange_id == "binance" else exchange_id.upper()
    accounts[exchange_id] = {
        "exchange": exchange_id,
        "apiKey": os.getenv(f"{key_prefix}_API_KEY"),
        "secret": os.getenv(f"{key_prefix}_API_SECRET"),
        "sandboxMode": True,
        "options": {"defaultType": "swap"},
    }

end_date = pd.Timestamp.now(tz="UTC").floor("1d")
start_date = end_date - pd.Timedelta(days=10)
symbols = ["BNB/USDT:USDT", "XRP/USDT:USDT"]

exchange = CCXTPandasMultiAccount(accounts=accounts)
ohlcv = exchange.fetch_ohlcv(symbol=symbols)
my_trades = exchange.fetch_my_trades(symbol=symbols, from_date=start_date, to_date=end_date)
funding = exchange.fetch_funding_history(symbol=symbols, from_date=start_date, to_date=end_date)
print(funding)
print(my_trades)

orders = ohlcv.drop_duplicates(subset=["symbol", "account"], keep="last")[
    ["symbol", "close", "account"]
].rename(columns={"close": "price"})
orders["price"] /= 2
orders["side"] = "buy"
orders["notional"] = 12
orders["type"] = "limit"
response = exchange.create_order(orders=orders)
print(response)
orders = exchange.fetch_open_orders(symbol=symbols)[
    ["id", "price", "amount", "side", "type", "symbol", "account"]
]
print(orders)
orders["amount"] *= 2
edit_response = exchange.edit_order(orders=orders)
print(edit_response)
cancel_response = exchange.cancel_order(orders=orders[["id", "symbol", "account"]])
print(cancel_response)
cancel_response = exchange.cancel_all_orders(symbol=symbols)
print(cancel_response)
