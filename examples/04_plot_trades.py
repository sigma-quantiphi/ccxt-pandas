"""Plot OHLCV candlesticks and trade scatter with Plotly.

Fetches OHLCV and trades for BNB/USDT:USDT from Binance and creates
interactive candlestick and trade scatter charts.
No API keys required — uses public market data.
"""

import ccxt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from ccxt_pandas import CCXTPandasExchange

exchange = ccxt.binance()
pandas_exchange = CCXTPandasExchange(exchange=exchange)
symbol = "BNB/USDT:USDT"

# OHLCV candlestick chart
df = pandas_exchange.fetch_ohlcv(symbol=symbol, timeframe="1h", limit=100)
fig = go.Figure(
    data=go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
    )
)
fig.update_layout(
    title="BNB/USDT:USDT OHLCV (Binance)",
    xaxis_title="Time",
    yaxis_title="Price (USDT)",
    xaxis_rangeslider_visible=False,
    template="plotly_dark",
)
fig.show()

# Trade scatter chart
df = pandas_exchange.fetch_trades(symbol=symbol)
df["amount"] = np.log1p(df["amount"]) * 10  # log scale size

fig = px.scatter(
    df, x="timestamp", y="price", size="amount", color="side", template="plotly_dark"
)
fig.show()
