# Explorer Dashboard

ccxt-pandas ships an optional Streamlit dashboard that lets you browse any CCXT
exchange method, see the resulting DataFrame, and copy the equivalent Python
snippet — useful for prototyping before writing scripts.

A hosted version is at [ccxt-explorer.com](https://www.ccxt-explorer.com/).

## Install

```bash
pip install "ccxt-pandas[explorer]"
```

Pulls in `streamlit`, `plotly`, and `Pillow`.

## Run

```bash
ccxt-pandas-explorer
# or
uv run ccxt-pandas-explorer
```

The CLI launches Streamlit on `http://localhost:8501` against the bundled app
at `ccxt_pandas_explorer/app.py`.

## What you can do

- **Pick any exchange** from the sidebar (~120 supported via CCXT).
- **Pick any `fetch_*` method** (the dropdown is built by introspecting
  `exchange.has` so only methods that actually work on that exchange show up).
- **Pick symbols** from the markets table (single- or multi-row selection
  depending on whether the method takes `symbol` or `symbols`).
- **Set parameters** — `timeframe`, `since`, `limit` etc. are auto-detected from
  the method signature.
- **See the DataFrame** post-conversion (UTC timestamps, numeric coercion,
  schema-validated shape).
- **Copy the equivalent code snippet** to paste into your own project.
- **Plot the result** with Plotly (line/bar/scatter, optional aggregation,
  facets, color, size).

## Adding credentials

The sidebar shows fields for whichever auth params the chosen exchange requires
(`apiKey`, `secret`, `password`, …). They are kept in Streamlit session state —
not persisted to disk. For private endpoints, paste them in; for public-only
endpoints (OHLCV, order books, trades), leave them blank.

## Sandbox mode

If the exchange supports a sandbox/testnet, a toggle appears in the sidebar.
Recommended for any test of order placement.

## Source

The app source is one self-contained file — see
[`ccxt_pandas_explorer/app.py`](https://github.com/sigma-quantiphi/ccxt-pandas/blob/main/ccxt_pandas_explorer/app.py).
Fork it, extend it, run your own version.
