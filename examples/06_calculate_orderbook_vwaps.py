"""Calculate order book VWAPs at various notional depths.

Fetches order books for all USDT pairs on Upbit, calculates VWAP
at several depth levels, and computes bid-ask spreads.
No API keys required — uses public market data.
"""

import ccxt
import pandas as pd

from ccxt_pandas import CCXTPandasExchange

pd.set_option("display.max_rows", 50)
pd.set_option("display.float_format", "{:.8f}".format)

exchange = ccxt.upbit()
pandas_exchange = CCXTPandasExchange(exchange=exchange)
markets = pandas_exchange.load_markets()
markets = markets.query("quote == 'USDT'")

desired_depths = [1_000, 10_000, 100_000, 1_000_000, 5_000_000]

orderbook = pandas_exchange.fetchOrderBooks().merge(markets)
print(orderbook)

# Calculate notional, cumulative depth, and max depth
orderbook["notional"] = orderbook["price"] * orderbook["qty"]
orderbook["cumNotional"] = orderbook.groupby(["symbol", "exchange", "side"])[
    "notional"
].cumsum()
orderbook["totalNotional"] = orderbook.groupby(["symbol", "exchange", "side"])[
    "notional"
].transform("sum")
orderbook["shiftCumNotional"] = orderbook["cumNotional"] - orderbook["notional"]

# Calculate orderbook VWAPs
vwaps = []
for depth in desired_depths:
    vwap = orderbook.query(f"shiftCumNotional <= {depth}").copy()
    vwap["notional"] = vwap["notional"].clip(upper=vwap["cumNotional"] - depth)
    vwap["depth"] = depth
    vwaps.append(vwap.copy())
vwaps = pd.concat(vwaps)
vwaps["qty"] = vwaps["notional"] / vwaps["price"]
vwaps = vwaps.groupby(["symbol", "exchange", "side", "depth"], as_index=False).agg(
    totalNotional=("totalNotional", "sum"),
    notional=("notional", "sum"),
    qty=("qty", "sum"),
)
vwaps["vwap"] = vwaps["notional"] / vwaps["qty"]
vwaps = vwaps.query("totalNotional >= depth")

# Calculate orderbook depth spreads
vwaps_pivot = vwaps.pivot(
    index=["symbol", "exchange", "depth"], columns="side", values="vwap"
).reset_index()
vwaps_pivot["spread"] = vwaps_pivot["asks"] - vwaps_pivot["bids"]
vwaps_pivot["spreadRelative"] = vwaps_pivot["spread"] / vwaps_pivot[
    ["asks", "bids"]
].mean(axis=1)
print(vwaps_pivot)

print("\nBTC/USDT:")
print(vwaps_pivot.query("symbol == 'BTC/USDT'"))
