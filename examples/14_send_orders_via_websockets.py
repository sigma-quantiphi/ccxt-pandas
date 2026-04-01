"""Send and edit orders via WebSocket.

Watches OHLCV via WebSocket, places a limit buy order on first tick,
then continuously edits the order price to track the market.
Requires BINANCE_SANDBOX_API_KEY and BINANCE_SANDBOX_API_SECRET in .env.
"""

import asyncio
import os

import ccxt.pro as ccxt_pro
from dotenv import load_dotenv

from ccxt_pandas import AsyncCCXTPandasExchange

load_dotenv()
exchange = ccxt_pro.binance(
    {
        "apiKey": os.environ["BINANCE_SANDBOX_API_KEY"],
        "secret": os.environ["BINANCE_SANDBOX_API_SECRET"],
    }
)
exchange.set_sandbox_mode(True)
pandas_exchange = AsyncCCXTPandasExchange(exchange=exchange)

symbol = "BNB/USDT"


async def main():
    sent_orders = False
    response = None
    while True:
        ohlcv = await pandas_exchange.watch_ohlcv(symbol=symbol)
        ohlcv = ohlcv.to_dict("records")[0]
        print(ohlcv)
        if not sent_orders:
            response = await exchange.create_order_ws(
                price=ohlcv["low"] - 10,
                amount=0.01,
                type="limit",
                side="buy",
                symbol=symbol,
            )
            print(response)
            sent_orders = True
        else:
            try:
                response = await exchange.edit_order_ws(
                    id=response["id"],
                    price=ohlcv["close"] - 10,
                    amount=0.01,
                    type="limit",
                    side="buy",
                    symbol=symbol,
                )
                print(response)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    asyncio.run(main())
