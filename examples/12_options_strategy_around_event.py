"""Build a BTC call calendar spread around a known event date.

Loads Binance USDT options, joins each contract with its current Greeks and
the underlying mark price, then picks the call closest to ATM on the
expiries just before and just after a target event (e.g. an FOMC decision).
The "sell" leg expires before the event; the "buy" leg expires after it.

No API keys required — uses public market data.
"""

import ccxt
import pandas as pd

from ccxt_pandas import CCXTPandasExchange

# Pick any event date in the future; the strategy is to sell the expiry
# just before it and buy the expiry just after.
event_date = pd.Timestamp.utcnow().normalize() + pd.Timedelta(days=14)

exchange = ccxt.binance({"options": {"defaultType": "option", "loadAllOptions": True}})
pandas_exchange = CCXTPandasExchange(exchange=exchange)

markets = pandas_exchange.load_markets().query("type == 'option' and quote == 'USDT'")[
    ["symbol", "base", "expiryDatetime", "strike", "optionType", "contractSize"]
]
greeks = pandas_exchange.fetch_all_greeks()
prices = (
    pandas_exchange.fetchMarkPrices()[["symbol", "indexPrice"]]
    .rename(columns={"symbol": "base"})
    .loc[lambda d: d["base"].str.contains("/USDT:USDT")]
    .assign(base=lambda d: d["base"].str.replace("/USDT:USDT", ""))
)

markets = markets.merge(prices).merge(greeks)
markets["strike_index_spread"] = (markets["strike"] - markets["indexPrice"]).abs()
markets["strike_index_spread_rel"] = markets["strike_index_spread"] / markets["indexPrice"]

calls = markets.query("base == 'BTC' and optionType == 'call'")

sell_leg = (
    calls.loc[calls["expiryDatetime"] < event_date]
    .sort_values(
        ["expiryDatetime", "strike_index_spread_rel"],
        ascending=[False, True],
        ignore_index=True,
    )
    .head(1)
)
buy_leg = (
    calls.loc[calls["expiryDatetime"] > event_date]
    .sort_values(["expiryDatetime", "strike_index_spread_rel"], ignore_index=True)
    .head(1)
)


def get_option_top_of_book(symbol: str) -> pd.DataFrame:
    return (
        pandas_exchange.fetch_order_book(symbol=symbol)
        .drop_duplicates(subset=["symbol", "side"])
        .pivot(index="symbol", columns="side", values="price")
        .reset_index()
        .assign(bid_ask_spread=lambda d: d["asks"] - d["bids"])
    )


sell_leg = sell_leg.merge(get_option_top_of_book(sell_leg["symbol"].iloc[0]))
buy_leg = buy_leg.merge(get_option_top_of_book(buy_leg["symbol"].iloc[0]))

print(f"Event date (UTC): {event_date}")
print("\nSell leg (expires before event):")
print(sell_leg.to_markdown(index=False))
print("\nBuy leg (expires after event):")
print(buy_leg.to_markdown(index=False))
