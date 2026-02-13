import asyncio
import time

import pandas as pd

from ccxt_pandas import AsyncCCXTPandasMultiExchange
from ccxt_pandas.utils.pandas_utils import async_concat_results

exchanges = AsyncCCXTPandasMultiExchange(
    exchange_names=(
        "binance",
        "bybit",
    )
)

# Define parameters
now = pd.Timestamp.now(tz="UTC")
end_date = now.floor("1h")
start_date = now.floor("1d") - pd.Timedelta(days=2)
symbols = ("BNB/USDT:USDT", "ETH/USDT:USDT")
timeframe = "1m"


async def main():
    ohlcv = exchanges.fetch_ohlcv(
        symbol=symbols, from_date=start_date, to_date=end_date
    )
    orderbook = exchanges.fetch_order_book(symbol=symbols)
    start_time = time.time()
    ohlcv, orderbook = await async_concat_results([ohlcv, orderbook])
    elapsed_time = time.time() - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
    print(ohlcv)
    print(orderbook)
    await asyncio.gather(*exchanges.close())


if __name__ == "__main__":
    asyncio.run(main())
