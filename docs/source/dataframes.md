# DataFrame Structures

Every supported `fetch_*` method returns a typed `pd.DataFrame`. Timestamps are
UTC `datetime64[ns, UTC]`; numeric fields are coerced from strings; booleans are
`bool` (not `0/1`). The exact shape per method is encoded in the [Pandera
schemas](api.rst) — re-exported from the package root:

```python
from ccxt_pandas import OHLCVSchema, OrderBookSchema, OrderSchema  # ... etc
```

This page is a quick visual reference for the most common shapes. For the
full list of schemas, see the API reference.

## OHLCV — `fetch_ohlcv`

| timestamp | open | high | low | close | volume |
|---|---|---|---|---|---|
| 2026-04-18 00:00:00+00:00 | 70000.0 | 70100.0 | 69950.0 | 70050.0 | 12.5 |

- One row per candle.
- `timestamp` is the **bar open** time, UTC.
- For multi-symbol calls, an extra `symbol` column is added.

## Order book — `fetch_order_book`

| symbol | side | price | qty |
|---|---|---|---|
| BTC/USDT | bids | 70000.0 | 1.5 |
| BTC/USDT | asks | 70050.0 | 1.0 |

- Long format (one row per level), not the nested `{bids: [...], asks: [...]}` ccxt shape.
- `side` is `"bids"` / `"asks"` (matching the ccxt convention).
- Use `sort_orderbook(df)` to get best bid/ask first within each `(symbol, side)`.

## Trades — `fetch_trades`, `fetch_my_trades`

| timestamp | symbol | id | side | price | amount | cost | fees | exchange |
|---|---|---|---|---|---|---|---|---|
| 2026-04-18 12:00:00.123+00:00 | BTC/USDT | 12345 | buy | 70000.0 | 0.01 | 700.0 | [...] | binance |

- `fees` is a list-of-dicts column (each fill may have multiple fees).

## Balance — `fetch_balance`

| currency | free | used | total |
|---|---|---|---|
| BTC | 0.5 | 0.1 | 0.6 |
| USDT | 1000.0 | 0.0 | 1000.0 |

- Long format, one row per currency. Filter empty rows with `.query("total > 0")`.

## Positions — `fetch_positions`

| symbol | side | contracts | notional | unrealizedPnl | leverage | marginMode | …  |
|---|---|---|---|---|---|---|---|

- Side is `"long"` / `"short"`.
- `contracts` is in contract units; `notional` is USD-equivalent.

## Orders — `fetch_open_orders`, `fetch_closed_orders`, `create_orders`

| id | symbol | side | type | price | amount | filled | status | timestamp |
|---|---|---|---|---|---|---|---|---|

- For batch operations, accept and return the same DataFrame shape — see [examples/00_sync_basics.py](https://github.com/sigma-quantiphi/ccxt-pandas/blob/main/examples/00_sync_basics.py).

## Markets — `load_markets`, `fetch_markets`

| symbol | base | quote | settle | type | subType | active | precision_price | precision_amount | limits_price_min | limits_price_max | limits_amount_min | limits_amount_max | limits_cost_min | limits_cost_max | …  |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

- One row per symbol. `type` is `"spot"`, `"swap"`, `"future"`, or `"option"`.
- Nested `precision`/`limits` dicts are flattened with `_` separators.

## Currencies — `fetch_currencies`

| id | code | name | precision | withdraw | deposit | network | network_id | network_fee | exchange |
|---|---|---|---|---|---|---|---|---|---|

- One row per `(currency, network)` combination — networks are exploded.
- Useful for routing transfers (see [examples/18_cheapest_withdrawal_route.py](https://github.com/sigma-quantiphi/ccxt-pandas/blob/main/examples/18_cheapest_withdrawal_route.py)).

## Funding rates — `fetch_funding_rates`, `fetch_funding_rate_history`

| symbol | timestamp | fundingRate | nextFundingTimestamp | indexPrice | markPrice |
|---|---|---|---|---|---|

## Greeks — `fetch_all_greeks`

| symbol | underlyingPrice | markPrice | bidPrice | askPrice | delta | gamma | theta | vega | impliedVolatility |
|---|---|---|---|---|---|---|---|---|---|

- Available for option-enabled exchanges (binance, bybit, okx, deribit).

## How shapes are determined

Each `fetch_*` method is registered in `ccxt_pandas/wrappers/method_mappings.py`
under one of these categories: `standard_methods`, `markets_methods`,
`currencies_methods`, `balance_methods`, `ohlcv_methods`,
`orderbook_methods`, `orders_methods`, `dict_methods`. The category determines
which `BaseProcessor` conversion path is used and which Pandera schema validates
the result.

Adding a new method to ccxt-pandas? See the [`add-supported-method`
skill](https://github.com/sigma-quantiphi/ccxt-pandas/blob/main/.claude/skills/add-supported-method.md).
