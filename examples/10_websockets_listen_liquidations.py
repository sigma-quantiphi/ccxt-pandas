"""WebSocket: listen to live liquidation events on OKX.

Streams liquidation data for all symbols via ccxt.pro WebSocket.
No API keys required — uses public market data.
"""

import asyncio

import ccxt.pro

from ccxt_pandas import AsyncCCXTPandasExchange

ex = AsyncCCXTPandasExchange(exchange=ccxt.pro.okx())


async def main():
    try:
        while True:
            df = await ex.watchLiquidationsForSymbols(symbols=None)
            print(df)
    except KeyboardInterrupt:
        await ex.exchange.close()
        print("Stopped by user.")
    except Exception as e:
        await ex.exchange.close()
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
