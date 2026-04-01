"""Async: fetch OHLCV for 1000 symbols in parallel.

Demonstrates AsyncCCXTPandasExchange with asyncio.gather for bulk data loading.
No API keys required — uses public market data only.
"""

import asyncio
import time

import ccxt.pro as ccxt_pro
import pandas as pd

from ccxt_pandas import AsyncCCXTPandasExchange

exchange = ccxt_pro.binance()
pandas_exchange = AsyncCCXTPandasExchange(exchange=exchange)


async def main():
    symbols = await pandas_exchange.load_markets()
    symbols = symbols.head(1000)
    print(symbols[["symbol", "base", "quote"]])

    tasks = [
        pandas_exchange.fetch_ohlcv(symbol=symbol, timeframe="1m", limit=1000)
        for symbol in symbols["symbol"]
    ]

    start_time = time.time()
    results = await asyncio.gather(*tasks, return_exceptions=True)
    await exchange.close()
    print(f"Execution time: {time.time() - start_time:.2f} seconds")

    results = pd.concat([r for r in results if isinstance(r, pd.DataFrame)])
    print(results)


if __name__ == "__main__":
    asyncio.run(main())
