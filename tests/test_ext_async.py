import os
import asyncio

import pandas as pd
from dotenv import load_dotenv
import ccxt.pro as ccxt

from ccxt_pandas import AsyncCCXTPandasExchange

load_dotenv()
api_key_read = os.getenv("SANDBOX_API_KEY")
api_secret_read = os.getenv("SANDBOX_API_SECRET")
exchange = ccxt.binance(
    {
        "apiKey": api_key_read,
        "secret": api_secret_read,
    }
)
exchange.set_sandbox_mode(True)
pandas_exchange = AsyncCCXTPandasExchange(
    exchange=exchange,
    max_number_of_orders=100,
)
symbols = ["BNB/USDT", "XRP/USDT"]


async def main():
    end_date = pd.Timestamp.now(tz="UTC").floor("1h")
    start_date = end_date - pd.Timedelta(days=5)
    ohlcv = await pandas_exchange.fetch_ohlcv(
        symbol=symbols, from_date=start_date, to_date=end_date
    )
    ohlcv = ohlcv.drop_duplicates(subset=["symbol"], keep="last")[
        ["symbol", "close"]
    ].rename(columns={"close": "price"})
    ohlcv["price"] /= 2
    ohlcv["side"] = "buy"
    ohlcv["notional"] = 12
    ohlcv["type"] = "limit"
    ohlcv = ohlcv.loc[ohlcv.index.repeat(3)].reset_index(drop=True)
    response = await pandas_exchange.create_order_from_dataframe(orders=ohlcv)
    print(response)
    orders = await pandas_exchange.fetch_open_orders(symbol=symbols)
    orders = orders[["id", "price", "amount", "side", "type", "symbol"]]
    print(orders)
    orders["amount"] *= 2
    orders = await pandas_exchange.edit_order_from_dataframe(orders=orders)
    print(orders)
    cancel_response = await pandas_exchange.cancel_order_from_dataframe(
        orders=orders[["id", "symbol"]]
    )
    print(cancel_response)
    orders = await pandas_exchange.create_orders_from_dataframe(orders=ohlcv)
    print(orders)
    orders = await pandas_exchange.fetch_open_orders(symbol=symbols)
    orders = orders[["id", "price", "amount", "side", "type", "symbol"]]
    print(orders)
    orders["amount"] *= 2
    await asyncio.sleep(3)
    orders = await pandas_exchange.edit_orders_from_dataframe(orders=orders)
    print(orders)
    cancel_response = await pandas_exchange.cancel_orders_from_dataframe(
        orders=orders[["id", "symbol"]]
    )
    print(cancel_response)
    orders = await pandas_exchange.create_orders_from_dataframe(orders=ohlcv)
    print(orders)
    orders = await pandas_exchange.cancel_all_orders(symbol=symbols)
    print(orders)
    await pandas_exchange.close()


if __name__ == "__main__":
    asyncio.run(main())
