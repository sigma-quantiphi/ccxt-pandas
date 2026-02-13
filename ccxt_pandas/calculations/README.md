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

## Future Additions

This module is designed to be extensible. Planned additions:

- **Risk calculations**: VaR, portfolio volatility, correlation matrices
- **Portfolio analytics**: Sharpe ratio, returns analysis, drawdown
- **Greeks calculations**: For options portfolios
- **Position tracking**: Unrealized PnL across instruments
