---
name: ccxt-pandas-helper
description: Helper for working with ccxt-pandas library in projects
---

You are helping with a project that uses ccxt-pandas, a wrapper around CCXT that returns pandas DataFrames instead of raw JSON/dicts.

## Key Architecture Concepts
- **Main classes**: `CCXTPandasExchange` (sync) and `AsyncCCXTPandasExchange` (async)
- **Method interception**: All CCXT methods are intercepted via `__getattribute__`
- **DataFrame conversion**: Responses automatically converted to DataFrames via `BaseProcessor`
- **Method categories**: Defined in `method_mappings.py` to route responses to correct conversion logic

## Installation & Setup
```bash
# Using uv
uv add ccxt-pandas

# Using pip
pip install ccxt-pandas
```

## Basic Usage Patterns

### Sync Exchange Wrapper
```python
from ccxt_pandas import CCXTPandasExchange
import ccxt

exchange = CCXTPandasExchange(ccxt.binance({
    'apiKey': 'YOUR_KEY',
    'secret': 'YOUR_SECRET',
    'enableRateLimit': True
}))

# All fetch methods return DataFrames
ohlcv_df = exchange.fetch_ohlcv('BTC/USDT', '1h')
balance_df = exchange.fetch_balance()
orders_df = exchange.fetch_open_orders()
```

### Async Exchange Wrapper
```python
from ccxt_pandas import AsyncCCXTPandasExchange
import ccxt.pro as ccxtpro

exchange = AsyncCCXTPandasExchange(ccxtpro.binance({
    'apiKey': 'YOUR_KEY',
    'secret': 'YOUR_SECRET'
}))

# Async/await pattern
async def fetch_data():
    ohlcv = await exchange.fetch_ohlcv('BTC/USDT', '1h')
    tickers = await exchange.fetch_tickers(['BTC/USDT', 'ETH/USDT'])
    await exchange.close()
    return ohlcv, tickers
```

## Common DataFrame Structures

### OHLCV Data
Columns: `timestamp`, `open`, `high`, `low`, `close`, `volume`, `symbol`

### Orders
Columns: `id`, `timestamp`, `symbol`, `type`, `side`, `price`, `amount`, `filled`, `remaining`, `status`, `trades`, `fees`

### Trades
Columns: `id`, `timestamp`, `symbol`, `side`, `price`, `amount`, `cost`

### Balance
Columns: `symbol`, `free`, `used`, `total`, `debt`

### Positions
Columns: `symbol`, `side`, `contracts`, `notional`, `leverage`, `unrealizedPnl`, `liquidationPrice`

## Batch Operations

### Create Multiple Orders from DataFrame
```python
import pandas as pd

orders_df = pd.DataFrame({
    'symbol': ['BTC/USDT', 'ETH/USDT'],
    'type': ['limit', 'limit'],
    'side': ['buy', 'sell'],
    'amount': [0.01, 0.1],
    'price': [50000, 3000]
})

results = exchange.create_orders_from_dataframe(orders_df)
```

### Cancel Multiple Orders from DataFrame
```python
orders_to_cancel = pd.DataFrame({
    'id': ['12345', '67890'],
    'symbol': ['BTC/USDT', 'ETH/USDT']
})

results = exchange.cancel_orders_from_dataframe(orders_to_cancel)
```

## Best Practices
1. **Use async for multiple concurrent requests** - much faster for fetching data from multiple symbols
2. **Enable rate limiting** - `'enableRateLimit': True` in exchange config
3. **Close async exchanges** - Always `await exchange.close()` when done
4. **Check exchange capabilities** - Not all exchanges support all methods
5. **Handle sandbox/testnet** - Set `'sandbox': True` for testing

## Common Issues & Solutions

### Issue: Method not found
**Solution**: Check if exchange supports the method: `exchange.has['fetchOHLCV']`

### Issue: Missing API credentials
**Solution**: Load from environment variables:
```python
import os
ccxt.binance({
    'apiKey': os.getenv('API_KEY'),
    'secret': os.getenv('API_SECRET')
})
```

### Issue: Rate limit errors
**Solution**: Enable rate limiting and/or reduce concurrency in async operations

## Testing
Projects using ccxt-pandas typically need API keys for testing. Set up `.env` file:
```
API_KEY=your_key_here
API_SECRET=your_secret_here
SANDBOX_API_KEY=sandbox_key  # for testnet
SANDBOX_API_SECRET=sandbox_secret
```

## Key Files in ccxt-pandas Projects
- `ccxt_pandas/wrappers/ccxt_pandas_exchange.py` - Sync wrapper implementation
- `ccxt_pandas/wrappers/async_ccxt_pandas_exchange.py` - Async wrapper implementation
- `ccxt_pandas/wrappers/method_mappings.py` - Method category registry
- `ccxt_pandas/wrappers/base_processor.py` - DataFrame conversion logic
- `ccxt_pandas/utils/pandas_utils.py` - DataFrame utilities and order preprocessing

When working with ccxt-pandas code, refer to these files for implementation details.
