"""Fetch and plot BTC volatility history from Deribit.

Fetches historical volatility data and creates a line chart.
No API keys required — uses public market data.
"""

import ccxt
import plotly.express as px

from ccxt_pandas import CCXTPandasExchange

exchange = ccxt.deribit()
pandas_exchange = CCXTPandasExchange(exchange=exchange)
df = pandas_exchange.fetch_volatility_history(code="BTC")
print(df)

fig = px.line(df, x="timestamp", y="volatility", title="BTC volatility")
fig.show()
