# Getting Started

## Install

```bash
pip install ccxt-pandas
```

Optional extras:

```bash
pip install "ccxt-pandas[explorer]"   # Streamlit dashboard
pip install "ccxt-pandas[mcp]"        # MCP server for AI assistants
pip install "ccxt-pandas[speed]"      # coincurve for faster signing
```

Requires Python 3.11 or newer.

## Three-line example

```python
import ccxt
from ccxt_pandas import CCXTPandasExchange

exchange = CCXTPandasExchange(exchange=ccxt.binance())
ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="1m", limit=1000)
```

`ohlcv` is a `pd.DataFrame` with columns `timestamp` (UTC `datetime64[ns]`), `open`, `high`, `low`, `close`, `volume` — already typed, no JSON wrangling.

## Async

```python
import asyncio
import ccxt.pro as ccxt
from ccxt_pandas import AsyncCCXTPandasExchange

async def main():
    async with AsyncCCXTPandasExchange(exchange=ccxt.binance()) as ex:
        ohlcv = await ex.fetch_ohlcv("BTC/USDT", timeframe="1m", limit=1000)
        async for trades in ex.watch_trades("BTC/USDT"):
            print(trades.tail())

asyncio.run(main())
```

## Authenticated calls

```python
import os
import ccxt
from ccxt_pandas import CCXTPandasExchange

exchange = CCXTPandasExchange(
    exchange=ccxt.binance(
        {
            "apiKey": os.environ["BINANCE_API_KEY"],
            "secret": os.environ["BINANCE_API_SECRET"],
        }
    )
)
balance = exchange.fetch_balance()
positions = exchange.fetch_positions()
```

Sandbox / testnet mode:

```python
exchange.exchange.set_sandbox_mode(True)
```

## Schema validation (opt-in)

Every supported method has a Pandera schema. Enable runtime validation:

```python
from ccxt_pandas import CCXTPandasExchange, OHLCVSchema

exchange = CCXTPandasExchange(
    exchange=ccxt.binance(),
    validate_schemas=True,    # validate every response
    strict_validation=True,   # raise on first violation (default: warn-only)
)
```

You can also validate a frame directly:

```python
OHLCVSchema.validate(my_dataframe)
```

## Multi-exchange and multi-account

```python
from ccxt_pandas import CCXTPandasMultiExchange, CCXTPandasMultiAccount

multi_exchange = CCXTPandasMultiExchange(exchange_names=("binance", "bybit", "okx"))
order_books = multi_exchange.fetch_order_book(symbol=["BTC/USDT", "ETH/USDT"])

multi_account = CCXTPandasMultiAccount(accounts={
    "binance_main": {"exchange": "binance", "apiKey": "...", "secret": "..."},
    "binance_alt":  {"exchange": "binance", "apiKey": "...", "secret": "..."},
})
balances = multi_account.fetch_balance()
```

## Where next

- [DataFrame structures](dataframes.md) — column reference for every method
- [Examples](examples.rst) — 20+ runnable scripts
- [Explorer dashboard](explorer.md) — interactive Streamlit UI
- [MCP server](mcp-server.md) — expose ccxt-pandas to Claude / other AI assistants
