import asyncio
import os

import pandas as pd
from dotenv import load_dotenv

from ccxt_pandas import AsyncCCXTPandasMultiAccount
from ccxt_pandas.utils.pandas_utils import async_concat_results

load_dotenv()
end_date = pd.Timestamp.now(tz="UTC").floor("1d")
start_date = end_date - pd.Timedelta(days=10)
symbols = ["BNB/USDT:USDT", "XRP/USDT:USDT"]
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
exchange = AsyncCCXTPandasMultiAccount(accounts=accounts)


async def main():
    ohlcv = exchange.fetch_ohlcv(symbol=symbols)
    orderbook = exchange.fetch_order_book(symbol=symbols)
    ohlcv, orderbook = await async_concat_results([ohlcv, orderbook])
    print(ohlcv)
    print(orderbook)
    orders = ohlcv.drop_duplicates(subset=["symbol", "account"], keep="last")[
        ["symbol", "close", "account"]
    ].rename(columns={"close": "price"})
    orders["price"] /= 2
    orders["side"] = "buy"
    orders["notional"] = 12
    orders["type"] = "limit"
    response = exchange.create_order(orders=orders)
    response = await async_concat_results(response)
    print(response)
    orders = exchange.fetch_open_orders(symbol=symbols)
    orders = await async_concat_results(orders)
    orders = orders[["id", "price", "amount", "side", "type", "symbol", "account"]]
    print(orders)
    orders["amount"] *= 2
    edit_response = exchange.edit_order(orders=orders)
    edit_response = await async_concat_results(edit_response)
    print(edit_response)
    cancel_response = exchange.cancel_order(orders=orders[["id", "symbol", "account"]])
    cancel_response = await async_concat_results(cancel_response)
    print(cancel_response)
    cancel_response = exchange.cancel_all_orders(symbol=symbols)
    cancel_response = await async_concat_results(cancel_response)
    print(cancel_response)
    response = await asyncio.gather(*exchange.close())
    print(response)


if __name__ == "__main__":
    asyncio.run(main())
