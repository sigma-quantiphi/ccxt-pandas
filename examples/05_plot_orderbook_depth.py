"""Plot order book depth chart with Plotly.

Fetches the order book for BNB/USDT:USDT and plots cumulative
quantity by price for bids and asks.
No API keys required — uses public market data.
"""

import ccxt
import plotly.express as px

from ccxt_pandas import CCXTPandasExchange

exchange = ccxt.binance()
pandas_exchange = CCXTPandasExchange(exchange=exchange)
symbol = "BNB/USDT:USDT"

df = pandas_exchange.fetch_order_book(symbol=symbol)
df["cumQty"] = df.groupby(["symbol", "side"])["qty"].cumsum()

fig = px.line(df, x="price", y="cumQty", color="side", template="plotly_dark")
fig.show()
