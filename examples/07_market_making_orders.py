"""Market making order examples: LIMIT_MAKER and QUEUE orders.

Demonstrates placing maker-only orders on Binance sandbox.
Requires BINANCE_SANDBOX_API_KEY and BINANCE_SANDBOX_API_SECRET in .env.
"""

import os

import ccxt
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("BINANCE_SANDBOX_API_KEY")
api_secret = os.getenv("BINANCE_SANDBOX_API_SECRET")

# Initialize exchange (sandbox)
binance = ccxt.binance(
    {
        "apiKey": api_key,
        "secret": api_secret,
        "enableRateLimit": True,
    }
)
binance.set_sandbox_mode(True)

# Place a LIMIT_MAKER spot order
print("Placing LIMIT_MAKER Spot Order...")
spot_order = binance.create_order(
    symbol="BTC/USDT",
    type="LIMIT_MAKER",
    side="sell",
    amount=0.001,
    price=100_000,
)
print(spot_order)

cancel = binance.cancel_order(symbol=spot_order["symbol"], id=spot_order["id"])
print(cancel)

# Place a perp order with matchPrice
print("Placing Perp Order with matchPrice: 'queue_20'...")
perp_order = binance.create_order(
    symbol="BTC/USDT:USDT",
    type="market",
    side="buy",
    amount=0.001,
    params={"matchPrice": "QUEUE_20"},
)
print("Perp Order Placed:", perp_order)
