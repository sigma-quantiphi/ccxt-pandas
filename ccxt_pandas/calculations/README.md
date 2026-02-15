# Calculations Module

This module provides higher-level calculation functions for common trading and risk management tasks, built on top of ccxt-pandas DataFrame outputs.

## Trade Analysis

### `aggregate_trades()`

Aggregate trades by specified columns with optional time resampling.

**Parameters:**
- `trades`: Trades DataFrame from `fetch_my_trades()`
- `group_by`: Columns to group by (default: `("symbol", "side")`)
- `freq`: Optional pandas frequency string for time aggregation (e.g., `"1H"`, `"1D"`)
- `include_fees`: Whether to include fee_cost in aggregation (default: `True`)

**Returns:**
- DataFrame with aggregated amounts, costs, fees, and trade counts

**Example:**

```python
import ccxt
import ccxt_pandas as cpd

exchange = cpd.CCXTPandasExchange(ccxt.binance())
trades = exchange.fetch_my_trades()

# Aggregate by symbol and side
summary = cpd.aggregate_trades(trades)
print(summary)
#     symbol  side  amount    cost  n_trades  fee_cost  signed_amount  signed_cost
# 0  BTC/USDT  buy     1.5   45000        10      45.0            1.5        45000.0
# 1  BTC/USDT  sell    1.0   31000         5      31.0           -1.0       -31000.0

# Aggregate by symbol only (combines buy/sell)
summary = cpd.aggregate_trades(trades, group_by=["symbol"])

# Hourly aggregation
hourly = cpd.aggregate_trades(trades, freq="1H")
```

**Use cases:**
- Summarize trading activity across symbols or time periods
- Analyze buy vs sell volumes
- Calculate net flows (signed_amount/signed_cost)
- Track trading frequency

---

### `calculate_realized_pnl()`

Calculate realized PnL metrics by matching buy and sell trades.

**Parameters:**
- `trades`: Trades DataFrame from `fetch_my_trades()`
- `group_by`: Columns to group by (default: `("symbol",)`)
- `freq`: Optional pandas frequency string for time aggregation
- `include_totals`: Whether to include "All" totals row (default: `False`)

**Returns:**
- DataFrame with buy/sell amounts, prices, spread, matched amounts, and realized PnL

**Example:**

```python
import ccxt
import ccxt_pandas as cpd

exchange = cpd.CCXTPandasExchange(ccxt.binance())
trades = exchange.fetch_my_trades()

# Calculate PnL per symbol
pnl = cpd.calculate_realized_pnl(trades)
print(pnl)
#     symbol  amount_buy  amount_sell  price_buy  price_sell  spread  amount_in_out  amount_net  pnl_in_out
# 0  BTC/USDT        1.5          1.0    30000.0     31000.0  1000.0            1.0         0.5      1000.0

# Daily PnL analysis
daily_pnl = cpd.calculate_realized_pnl(trades, freq="1D")

# Include totals row
pnl = cpd.calculate_realized_pnl(trades, include_totals=True)
```

**Output columns:**
- `amount_buy`, `amount_sell`: Total amounts per side
- `price_buy`, `price_sell`: Average prices (cost/amount)
- `spread`: Price difference (sell - buy)
- `amount_in_out`: Matched amount (min of buy/sell)
- `amount_net`: Net position (buy - sell, shows inventory)
- `pnl_in_out`: Realized PnL (matched_amount × spread)

**Use cases:**
- Track realized profits/losses
- Analyze average entry/exit prices
- Monitor spread capture
- Identify net positions (inventory)
- Calculate performance metrics

---

## Order Book Analysis

### `calculate_vwap_by_depth()`

Calculate Volume-Weighted Average Price (VWAP) at various depth levels. Useful for estimating market impact and slippage.

**Parameters:**
- `df`: Order book DataFrame with price, qty, symbol, and side columns
- `depths`: List of notional depths to calculate VWAP for (e.g., `[1000, 5000, 10000]`)
- `group_by`: Columns to group by (default: `['symbol', 'side']` + `'exchange'` if present)
- `price_col`: Name of price column (default: `'price'`)
- `qty_col`: Name of quantity column (default: `'qty'`)

**Returns:**
- DataFrame with columns: `[*group_by, depth, qty, notional, price]` where `'price'` is the VWAP

**Example:**

```python
import ccxt
import ccxt_pandas as cpd

exchange = cpd.CCXTPandasExchange(ccxt.binance())
orderbook = exchange.fetch_order_book('BTC/USDT')

# Sort the order book first
sorted_ob = cpd.sort_orderbook(orderbook)

# Calculate VWAP for buying $1,000, $5,000, and $10,000 worth
vwap = cpd.calculate_vwap_by_depth(sorted_ob, depths=[1000, 5000, 10000])
print(vwap)
#     symbol  side   depth      qty  notional     price
# 0  BTC/USDT  asks  1000.0    0.015    1000.0  66666.67
# 1  BTC/USDT  asks  5000.0    0.075    5000.0  66666.67
# 2  BTC/USDT  asks 10000.0    0.150   10000.0  66667.50
```

**How it works:**
1. Calculates cumulative notional within each group
2. For each depth level, includes all levels where cumulative notional - current notional ≤ depth
3. Adjusts the last level for partial fills
4. Calculates VWAP as total notional / total quantity

**Use cases:**
- Market impact analysis - what price will I get for a large order?
- Slippage estimation - how much worse than best price?
- Liquidity assessment - is there enough depth at good prices?
- Order size optimization - find optimal size before excessive slippage

---

### `calculate_mid_price()`

Calculate mid price from order book for all symbols (average of best bid and best ask).

**Parameters:**
- `data`: Order book DataFrame (should be sorted)
- `price_col`: Name of price column (default: `'price'`)
- `by_exchange`: Include exchange in grouping (default: `False`)

**Returns:**
- DataFrame with `'mid_price'` column, indexed by symbol (and optionally exchange)

**Example:**

```python
import ccxt
import ccxt_pandas as cpd

exchange = cpd.CCXTPandasExchange(ccxt.binance())
orderbook = exchange.fetch_order_book('BTC/USDT')
sorted_ob = cpd.sort_orderbook(orderbook)

mid = cpd.calculate_mid_price(sorted_ob)
print(mid)
#            mid_price
# symbol
# BTC/USDT   66666.00

# Multiple symbols
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
orderbooks = [exchange.fetch_order_book(s) for s in symbols]
combined = pd.concat(orderbooks)
sorted_ob = cpd.sort_orderbook(combined)
mid = cpd.calculate_mid_price(sorted_ob)
print(mid)
#            mid_price
# symbol
# BTC/USDT   66666.00
# ETH/USDT    3500.00
# SOL/USDT     100.00
```

**Use cases:**
- Fair value estimation across multiple symbols
- Spread calculation baseline
- Mark price alternative
- Cross-exchange arbitrage comparison

---

### `calculate_spread()`

Calculate bid-ask spread from order book for all symbols.

**Parameters:**
- `data`: Order book DataFrame (should be sorted)
- `price_col`: Name of price column (default: `'price'`)
- `relative`: Return as percentage of mid price (default: `False`)
- `by_exchange`: Include exchange in grouping (default: `False`)

**Returns:**
- DataFrame with `'spread'` column, indexed by symbol (and optionally exchange)

**Example:**

```python
import ccxt
import ccxt_pandas as cpd

exchange = cpd.CCXTPandasExchange(ccxt.binance())

# Multiple symbols
symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']
orderbooks = [exchange.fetch_order_book(s) for s in symbols]
combined = pd.concat(orderbooks)
sorted_ob = cpd.sort_orderbook(combined)

# Absolute spread
spread_abs = cpd.calculate_spread(sorted_ob)
print(spread_abs)
#            spread
# symbol
# BTC/USDT     1.00
# ETH/USDT     0.50
# SOL/USDT     0.01

# Relative spread (as percentage of mid price)
spread_rel = cpd.calculate_spread(sorted_ob, relative=True)
print(spread_rel * 100)  # Convert to percentage
#            spread
# symbol
# BTC/USDT    0.015
# ETH/USDT    0.014
# SOL/USDT    0.010
```

**Use cases:**
- Liquidity assessment across symbols - tighter spreads = more liquid
- Trading cost estimation - minimum cost to round-trip
- Exchange comparison - which has better pricing?
- Market making feasibility - is the spread wide enough?

---

### `sort_orderbook()`

Sort order book by symbol, side, and price levels. Ensures best bid (highest price) and best ask (lowest price) appear first.

**Parameters:**
- `df`: Order book DataFrame with `'symbol'`, `'side'`, and price columns
- `by_symbol`: Include symbol in sort (default: `True`)
- `by_exchange`: Include exchange in sort (default: `False`)
- `price_col`: Name of price column (default: `'price'`)

**Returns:**
- Sorted DataFrame with best prices first

**Example:**

```python
import ccxt
import ccxt_pandas as cpd

exchange = cpd.CCXTPandasExchange(ccxt.binance())
orderbook = exchange.fetch_order_book('BTC/USDT')

# Sort the order book
sorted_ob = cpd.sort_orderbook(orderbook)
print(sorted_ob.head())
#     symbol  side     price     qty
# 0  BTC/USDT  bids  66665.0  0.5000  <- Best bid (highest)
# 1  BTC/USDT  bids  66664.0  1.2000
# 2  BTC/USDT  asks  66666.0  0.3000  <- Best ask (lowest)
# 3  BTC/USDT  asks  66667.0  0.8000
```

**Use cases:**
- Prepare order book for analysis (always sort first!)
- Find best bid/ask prices
- Calculate spreads and depth metrics
- Visualize order book levels

---

### `calculate_notional()`

Calculate notional value (price × quantity) for order book levels.

**Parameters:**
- `df`: DataFrame with price and quantity columns
- `price_col`: Name of price column (default: `'price'`)
- `qty_col`: Name of quantity column (default: `'qty'`)

**Returns:**
- Series with notional values

**Example:**

```python
import ccxt
import ccxt_pandas as cpd
import pandas as pd

orderbook = pd.DataFrame({
    'price': [100, 101, 102],
    'qty': [1.5, 2.0, 1.0]
})

notional = cpd.calculate_notional(orderbook)
print(notional)
# 0    150.0
# 1    202.0
# 2    102.0
```

**Use cases:**
- Calculate order book depth in dollar terms
- VWAP calculations
- Liquidity analysis

---

### `signed_price()`

Calculate signed price based on side. Multiplies price by +1 for asks/sell, -1 for bids/buy. Useful for sorting order books.

**Parameters:**
- `df`: DataFrame with `'side'` and price columns
- `price_col`: Name of price column (default: `'price'`)

**Returns:**
- Series with signed prices

**Example:**

```python
import pandas as pd
import ccxt_pandas as cpd

orderbook = pd.DataFrame({
    'side': ['bids', 'asks', 'bids'],
    'price': [99.5, 100.5, 99.0]
})

signed = cpd.signed_price(orderbook)
print(signed)
# 0    -99.5
# 1    100.5
# 2    -99.0
```

**Use cases:**
- Order book sorting (best bid and best ask both sort first)
- Spread calculations
- Distance from mid calculations

---

### `side_sign()`

Get directional sign for order book sides. Returns +1 for asks/sell, -1 for bids/buy.

**Parameters:**
- `df`: DataFrame with `'side'` column

**Returns:**
- Series with +1 for asks/sell, -1 for bids/buy

**Example:**

```python
import pandas as pd
import ccxt_pandas as cpd

orderbook = pd.DataFrame({'side': ['bids', 'asks', 'bids']})
signs = cpd.side_sign(orderbook)
print(signs)
# 0   -1
# 1    1
# 2   -1
```

**Use cases:**
- Signed calculations (prices, quantities)
- Direction-aware aggregations

---

### `is_ask_side()`

Identify ask side rows in order book. Handles both order book format (`'asks'`/`'bids'`) and order format (`'sell'`/`'buy'`).

**Parameters:**
- `df`: DataFrame with `'side'` column

**Returns:**
- Boolean Series where `True` indicates ask/sell side

**Example:**

```python
import pandas as pd
import ccxt_pandas as cpd

orderbook = pd.DataFrame({'side': ['bids', 'asks', 'buy', 'sell']})
is_ask = cpd.is_ask_side(orderbook)
print(is_ask)
# 0    False
# 1     True
# 2    False
# 3     True
```

**Use cases:**
- Filter to one side of the order book
- Side-specific calculations
- Validation checks

---

### `create_mirrored_sides()`

Create mirrored order book sides for testing or simulation. Takes a DataFrame and duplicates it for each side.

**Parameters:**
- `df`: DataFrame with order data (price, qty, etc.)
- `sides`: Tuple of side values to create (default: `("buy", "sell")`)

**Returns:**
- DataFrame with rows duplicated for each side

**Example:**

```python
import pandas as pd
import ccxt_pandas as cpd

orders = pd.DataFrame({'price': [100, 101], 'qty': [1.0, 2.0]})
mirrored = cpd.create_mirrored_sides(orders)
print(mirrored)
#    price  qty  side
# 0    100  1.0   buy
# 1    101  2.0   buy
# 2    100  1.0  sell
# 3    101  2.0  sell
```

**Use cases:**
- Creating symmetric order books for testing
- Simulating market making scenarios
- Testing spread strategies

---

## Delta Hedging

### `calculate_delta_exposure()`

Calculate net delta exposure across spot, swap, and futures positions. Useful for delta-neutral hedging strategies.

**Parameters:**
- `balance`: Balance DataFrame from `fetch_balance()`
- `positions`: Positions DataFrame from `fetch_positions()`
- `markets`: Markets DataFrame from `load_markets()`
- `base_column`: Column name for base currency (default: `'base'`)
- `code_column`: Column name for currency code in balance (default: `'code'`)
- `amount_column`: Column name for amount/quantity (default: `'amount'`)

**Returns:**
- DataFrame with net exposure in each base currency

**Example:**

```python
import ccxt
import ccxt_pandas as cpd

# Initialize exchange wrapper
exchange = cpd.CCXTPandasExchange(ccxt.binance())

# Fetch data
balance = exchange.fetch_balance()
positions = exchange.fetch_positions()
markets = exchange.load_markets()

# Calculate delta exposure
delta = cpd.calculate_delta_exposure(balance, positions, markets)

print(delta)
#    base    amount
# 0  BTC   1.234567
# 1  ETH  12.345678
# 2  USDT  1000.00
```

**How it works:**

1. Merges market data onto positions to get base currency
2. Calculates signed amounts for positions:
   - Long positions: positive amount
   - Short positions: negative amount
3. Multiplies by contract size for derivatives
4. Combines spot balances with position amounts
5. Sums by base currency to get net exposure

**Use cases:**

- **Delta-neutral trading**: Identify imbalances to hedge
- **Portfolio risk**: See total exposure per asset
- **Rebalancing**: Calculate required trades to achieve target delta
- **Multi-leg strategies**: Combine spot + perpetual + futures positions

---

## Precision & Rounding

### `floor_series()`

Round Series values down to specified decimal places.

**Parameters:**
- `data`: Series to round
- `digits`: Number of decimal places (default: `0`)

**Returns:**
- Series with values rounded down

**Example:**

```python
import ccxt_pandas as cpd
import pandas as pd

prices = pd.Series([1.2345, 2.6789, 3.9999])

# Round down to 2 decimals
floored = cpd.floor_series(prices, digits=2)
print(floored)
# 0    1.23
# 1    2.67
# 2    3.99

# Round down to integer
floored = cpd.floor_series(prices)
print(floored)
# 0    1.0
# 1    2.0
# 2    3.0
```

**Use cases:**
- Price precision requirements
- Rounding amounts down to exchange limits
- Ensuring minimum tick sizes

---

### `ceil_series()`

Round Series values up to specified decimal places.

**Parameters:**
- `data`: Series to round
- `digits`: Number of decimal places (default: `0`)

**Returns:**
- Series with values rounded up

**Example:**

```python
import ccxt_pandas as cpd
import pandas as pd

prices = pd.Series([1.2345, 2.6789, 3.0001])

# Round up to 2 decimals
ceiled = cpd.ceil_series(prices, digits=2)
print(ceiled)
# 0    1.24
# 1    2.68
# 2    3.01

# Round up to integer
ceiled = cpd.ceil_series(prices)
print(ceiled)
# 0    2.0
# 1    3.0
# 2    4.0
```

**Use cases:**
- Minimum order size requirements
- Ensuring amounts meet exchange minimums
- Conservative rounding for risk management

---

## Future Additions

This module is designed to be extensible. Planned additions:

- **Risk calculations**: VaR, portfolio volatility, correlation matrices
- **Portfolio analytics**: Sharpe ratio, returns analysis, drawdown
- **Greeks calculations**: For options portfolios
- **Position tracking**: Unrealized PnL across instruments
