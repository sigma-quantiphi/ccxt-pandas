"""Spot/Future/Swap price spread and volume analysis with Plotly.

Fetches BTC OHLCV across spot, futures, and swap markets on Binance,
calculates spread to BTC/USDT spot, and visualizes with stacked volume.
No API keys required — uses public market data.
"""

import ccxt
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ccxt_pandas import CCXTPandasExchange

# Initialize the Binance exchange
exchange = ccxt.binance()
pandas_exchange = CCXTPandasExchange(exchange=exchange)

# Load and filter markets
markets = pandas_exchange.load_markets().query(
    "base == 'BTC' and quote in ['USDT', 'USDC', 'USD']"
)[["symbol", "type", "subType"]]
symbols = markets["symbol"].tolist()
print(markets)

# Fetch OHLCV
ohlcvs = []
for symbol in symbols:
    df = pandas_exchange.fetch_ohlcv(symbol=symbol, timeframe="1h", limit=100)
    df["symbol"] = symbol
    ohlcvs.append(df.copy())
ohlcv = pd.concat(ohlcvs)[["timestamp", "symbol", "close", "volume"]]

ohlcv = ohlcv.merge(markets, on="symbol")

# Get BTC/USDT spot price as reference
spot = (
    ohlcv.query("symbol == 'BTC/USDT'")[["timestamp", "close"]]
    .copy()
    .rename(columns={"close": "BTC/USDT"})
)
ohlcv = ohlcv.merge(spot, on="timestamp", how="left")
ohlcv["spread"] = ohlcv["close"] - ohlcv["BTC/USDT"]

# Create figure with subplots
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    row_heights=[0.6, 0.4],
    specs=[[{"secondary_y": True}], [{}]],
    vertical_spacing=0.05,
    subplot_titles=(
        "Spread to BTC/USDT (L) and BTC/USDT Price (R)",
        "Stacked Volume by Contract",
    ),
)
added_legendgroups = set()

legend_titles = {
    "spot-None": "Spot",
    "future-linear": "Futures (Linear)",
    "future-inverse": "Futures (Inverse)",
    "swap-linear": "Swap (Linear)",
    "swap-inverse": "Swap (Inverse)",
}

# --- Price Spread (L) and BTC/USDT Price (R) ---
for symbol, group in ohlcv.groupby("symbol"):
    if symbol != "BTC/USDT":
        symbol_meta = group.iloc[0]
        legend_group = f"{symbol_meta['type']}-{symbol_meta['subType']}"
        legend_title = legend_titles.get(legend_group, legend_group)

        legend_title_arg = (
            {"legendgrouptitle_text": legend_title}
            if legend_group not in added_legendgroups
            else {}
        )
        added_legendgroups.add(legend_group)

        fig.add_trace(
            go.Scatter(
                x=group["timestamp"],
                y=group["spread"],
                name=f"{symbol} Spread",
                mode="lines",
                legendgroup=legend_group,
                showlegend=True,
                **legend_title_arg,
            ),
            row=1,
            col=1,
            secondary_y=False,
        )

# BTC/USDT reference price
fig.add_trace(
    go.Scatter(
        x=spot["timestamp"],
        y=spot["BTC/USDT"],
        name="BTC/USDT Price",
        mode="lines",
        line=dict(dash="dot", width=2),
        legendgroup="spot-reference",
        showlegend=True,
    ),
    row=1,
    col=1,
    secondary_y=True,
)

# --- Stacked Volume ---
for symbol, group in ohlcv.groupby("symbol"):
    symbol_meta = group.iloc[0]
    legend_group = f"{symbol_meta['type']}-{symbol_meta['subType']}"
    legend_title = legend_titles.get(legend_group, legend_group)

    legend_title_arg = (
        {"legendgrouptitle_text": legend_title} if legend_group not in added_legendgroups else {}
    )
    added_legendgroups.add(legend_group)

    fig.add_trace(
        go.Bar(
            x=group["timestamp"],
            y=group["volume"],
            name=f"{symbol} Vol",
            legendgroup=legend_group,
            showlegend=True,
            **legend_title_arg,
        ),
        row=2,
        col=1,
    )

fig.update_layout(
    title="BTC Contract Spreads vs BTC/USDT + Volume Overview",
    height=800,
    barmode="stack",
    hovermode="x unified",
    hoverlabel=dict(namelength=-1),
    legend=dict(orientation="h", yanchor="bottom", y=-1, xanchor="right", x=1),
)
fig.update_yaxes(title_text="Spread to BTC/USDT", row=1, col=1, secondary_y=False)
fig.update_yaxes(title_text="BTC/USDT Price", row=1, col=1, secondary_y=True)
fig.update_yaxes(title_text="Volume", row=2, col=1)

fig.show()
