# Calculations Module

This module provides higher-level calculation functions for common trading and risk management tasks, built on top of ccxt-pandas DataFrame outputs.

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

## Future Additions

This module is designed to be extensible. Planned additions:

- **Risk calculations**: VaR, portfolio volatility, correlation matrices
- **Portfolio analytics**: Sharpe ratio, returns analysis, drawdown
- **Greeks calculations**: For options portfolios
- **PnL tracking**: Realized/unrealized PnL across instruments
