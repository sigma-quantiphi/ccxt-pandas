"""Async: load markets from all CCXT exchanges in parallel.

Demonstrates AsyncCCXTPandasExchange with every supported exchange.
No API keys required — uses public market data only.
"""

import asyncio
import time

import ccxt.pro as ccxt_pro
import pandas as pd

from ccxt_pandas import AsyncCCXTPandasExchange


async def main():
    exchanges = []
    tasks = []
    close_tasks = []

    for exchange_name in ccxt_pro.exchanges:
        exchange_class = getattr(ccxt_pro, exchange_name)
        exchange = exchange_class({"enableRateLimit": True})
        exchanges.append(exchange)
        pandas_exchange = AsyncCCXTPandasExchange(exchange=exchange)
        tasks.append(pandas_exchange.load_markets())
        close_tasks.append(exchange.close())

    print(f"Loading markets from {len(tasks)} exchanges...")
    start_time = time.time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(f"Fetch time: {time.time() - start_time:.2f} seconds")

    start_time = time.time()
    await asyncio.gather(*close_tasks, return_exceptions=True)
    print(f"Close time: {time.time() - start_time:.2f} seconds")

    dataframes = [r for r in results if isinstance(r, pd.DataFrame)]
    combined = pd.concat(dataframes)
    print(f"Total markets: {len(combined)}")
    print(combined)


if __name__ == "__main__":
    asyncio.run(main())
