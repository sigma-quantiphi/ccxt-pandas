# CCXT-Pandas

![Python version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![GitHub](https://img.shields.io/badge/github-Visit&nbsp;Repo-black?style=for-the-badge&logo=github)](https://github.com/sigma-quantiphi/ccxt-pandas)
[![PyPI version](https://badge.fury.io/py/ccxt-pandas.svg)](https://pypi.org/project/ccxt-pandas/)
[![Downloads](https://static.pepy.tech/personalized-badge/ccxt-pandas?period=month&units=international_system&left_color=grey&right_color=blue&left_text=downloads/month)](https://pepy.tech/project/ccxt-pandas)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sigma-quantiphi/ccxt-pandas/HEAD?urlpath=%2Fdoc%2Ftree%2Fexamples)
[![Explore Data](https://img.shields.io/badge/Explore%20Data-CCXT--Explorer-ffffff?logo=streamlit&style=plastic&color=ffffff&logoColor=FF4B4B)](https://www.ccxt-explorer.com/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sigma-quantiphi/ccxt-pandas/blob/main/LICENSE.md)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![CI](https://github.com/sigma-quantiphi/ccxt-pandas/actions/workflows/ci.yml/badge.svg)](https://github.com/sigma-quantiphi/ccxt-pandas/actions/workflows/ci.yml)
[![Docs](https://github.com/sigma-quantiphi/ccxt-pandas/actions/workflows/docs.yml/badge.svg)](https://sigma-quantiphi.github.io/ccxt-pandas/)
[![Medium badge](https://img.shields.io/badge/-Follow&nbsp;on&nbsp;Medium-black?style=social&logo=medium)](https://medium.com/@lucasjamar47)

## 🚀 CCXT → Pandas DataFrames in One Line
No more JSON → DataFrame glue code.
Every CCXT method returns a clean, typed pandas DataFrame.

```python
import ccxt
from ccxt_pandas import CCXTPandasExchange

exchange = CCXTPandasExchange(exchange=ccxt.binance())
ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="1m", limit=1000)
plt = ohlcv.close.plot(title="BTC/USDT — 1m")
plt.show()
```

## Why CCXT-Pandas?
CCXT-Pandas fuses the power of [Pandas](https://pandas.pydata.org/) with the market-connectivity of [CCXT](https://github.com/ccxt/ccxt/).
It turns CCXT’s nested JSONs into clean, typed DataFrames for analysis, backtests, or dashboards.
It lets you place/cancel live orders using the same DataFrame-centric API.

1-liners, everywhere. Fetch OHLCV, tickers, trades, order books, balances, orders → all as DataFrames.

* Consistent columns & dtypes. Timestamps as UTC datetime64[ns, UTC], numeric columns as proper numerics.
* Zero boilerplate. Stop writing JSON-to-DataFrame glue for every exchange.
* CCXT-compatible. Keep your favorite CCXT params; just get DataFrames back.

## Installation

CCXT-Pandas can be installed on Python 3.11~3.14:

```bash
pip install ccxt-pandas
```

## Examples

See the [`examples/`](examples/) directory for 20 runnable examples covering market data, trading, analytics, and WebSocket streaming. Most ship as paired `.py` + `.ipynb` files (open the notebook in [Binder](https://mybinder.org/v2/gh/sigma-quantiphi/ccxt-pandas/HEAD?urlpath=%2Fdoc%2Ftree%2Fexamples) for inline plots); the 4 async / WebSocket examples (10, 14, 16, 17) are `.py`-only because Jupyter's running event loop breaks `asyncio.run()`.

| # | Notebook | Description | Auth? |
|---|--------|-------------|-------|
| 00 | [Sync basics](examples/00_sync_basics.ipynb) | OHLCV, order books, trades, funding rates, batch orders | Yes |
| 01 | [Spot/Future/Swap Analysis](examples/01_spot_future_swap_price_volume_analysis.ipynb) | BTC spread and volume across contract types | No |
| 02 | [Exchange Arbitrage](examples/02_exchange_arbitrage.ipynb) | Cross-exchange spread detection | No |
| 03 | [Fetch Private Data](examples/03_fetch_private_data.ipynb) | Trades, positions, greeks | Yes |
| 04 | [Plot Trades](examples/04_plot_trades.ipynb) | OHLCV candlestick + trade scatter charts | No |
| 05 | [Orderbook Depth](examples/05_plot_orderbook_depth.ipynb) | Cumulative depth chart | No |
| 06 | [Orderbook VWAPs](examples/06_calculate_orderbook_vwaps.ipynb) | VWAP at multiple notional depths | No |
| 07 | [Market Making](examples/07_market_making_orders.ipynb) | LIMIT_MAKER and QUEUE orders | Yes |
| 08 | [Coin-Quoted Pricing](examples/08_pricing_coin_quoted_symbols.ipynb) | Convert to USDT-equivalent prices | No |
| 09 | [Deposits/Withdrawals](examples/09_deposits_withdrawals.ipynb) | Fetch deposit/withdrawal history | Yes |
| 10 | [WS Liquidations](examples/10_websockets_listen_liquidations.py) (`.py`) | Stream live liquidation events | No |
| 11 | [Volatility History](examples/11_fetch_volatility_history.ipynb) | BTC volatility from Deribit | No |
| 12 | [Options Calendar Spread](examples/12_options_strategy_around_event.ipynb) | Pick BTC call legs around an event date | No |
| 13 | [Delta Position](examples/13_delta_position.ipynb) | Net delta across spot + derivatives | Yes |
| 14 | [WS Orders](examples/14_send_orders_via_websockets.py) (`.py`) | Place/edit orders via WebSocket | Yes |
| 15 | [Open Interest](examples/15_open_interest_history.ipynb) | Historical open interest + pct change | No |
| 16 | [1000 OHLCV Async](examples/16_load_1000_ohlcv_async.py) (`.py`) | Bulk OHLCV with `asyncio.gather` | No |
| 17 | [All Exchanges Async](examples/17_load_symbols_all_exchanges_async.py) (`.py`) | Load markets from every exchange | No |
| 18 | [Cheapest Withdrawal Route](examples/18_cheapest_withdrawal_route.ipynb) | Cheapest cross-exchange transfer rail per currency | Yes |
| 19 | [Multi-Exchange Greeks](examples/19_multi_exchange_greeks.ipynb) | Aggregate option Greeks across binance/bybit/okx | No |
| 20 | [Trade Caching](examples/20_caching_repeat_fetches.ipynb) | `cache=True` for incremental `fetch_trades` | No |

## Getting Started

CCXT-Pandas works identically to CCXT. Just add `exchange = CCXTPandasExchange(exchange=exchange)`
and the exchange methods provided by CCXT will be exposed to CCXT-Pandas.

### Sync

```python
import ccxt
from ccxt_pandas import CCXTPandasExchange

# Initialize a CCXTPandasExchange object
exchange = ccxt.binance(dict(apiKey="your_api_key_here", secret="your_secret_here"))
exchange = CCXTPandasExchange(exchange=exchange)

# OHLCV
ohlcv = exchange.fetch_ohlcv("BTC/USDT", timeframe="1m", limit=100)      # -> DataFrame
# Trades
trades = exchange.fetch_trades("BTC/USDT", limit=1000)                   # -> DataFrame
# Orderbook
ob = exchange.fetch_order_book("BTC/USDT", limit=50)                 # -> DataFrame
# Tickers
tick = exchange.fetch_tickers()                               # -> DataFrame

# Fetch open orders from an exchange
open_orders = exchange.fetch_open_orders(symbol="BTC/USDT")

# Halve the amount and edit orders
open_orders["amount"] /= 2
response = exchange.edit_orders(open_orders)

# Display the transformed orders dataframe
print(response)
```

### Async

```
import asyncio
import ccxt.pro as ccxtpro
from ccxt_pandas import AsyncCCXTPandasExchange

ex = AsyncCCXTPandasExchange(ccxtpro.okx())

async def main():
    while True:
        trades = await ex.watch_trades("BTC/USDT")
        print(trades)

if __name__ == "__main__":
    asyncio.run(main())
```

## Explorer Dashboard

CCXT-Pandas ships an optional Streamlit dashboard for browsing any CCXT exchange method, copying the equivalent code snippet, and plotting the resulting DataFrame. The hosted version lives at [ccxt-explorer.com](https://www.ccxt-explorer.com/).

### Installation

```bash
pip install ccxt-pandas[explorer]
```

### Running

```bash
# Via CLI
ccxt-pandas-explorer

# Via uv
uv run ccxt-pandas-explorer
```

## MCP Server

CCXT-Pandas includes an optional MCP (Model Context Protocol) server that exposes exchange data and trading as tools for AI assistants like Claude.

### Installation

```bash
pip install ccxt-pandas[mcp]
```

### Configuration

Create a config file (e.g. `ccxt-mcp-config.json`):

```json
{
  "accounts": {
    "binance": {
      "exchange": "binance",
      "api_key": "your_api_key",
      "secret": "your_secret",
      "sandbox_mode": true
    }
  },
  "read_only": true
}
```

Or use environment variables:

```bash
export CCXT_MCP_ACCOUNT_BINANCE_EXCHANGE=binance
export CCXT_MCP_ACCOUNT_BINANCE_API_KEY=your_key
export CCXT_MCP_ACCOUNT_BINANCE_SECRET=your_secret
export CCXT_MCP_READ_ONLY=true
```

### Running

```bash
# Via CLI
ccxt-pandas-mcp

# Via uv
uv run ccxt-pandas-mcp
```

### Claude Desktop / Claude Code

Add to your MCP client config:

```json
{
  "mcpServers": {
    "ccxt-pandas": {
      "command": "uv",
      "args": ["run", "ccxt-pandas-mcp"],
      "env": {
        "CCXT_MCP_CONFIG": "/path/to/ccxt-mcp-config.json"
      }
    }
  }
}
```

### Available Tools

| Category | Tools |
|----------|-------|
| **Exchange Info** | `list_exchanges`, `load_markets`, `fetch_currencies` |
| **Market Data** | `fetch_ohlcv`, `fetch_trades`, `fetch_order_book`, `fetch_ticker`, `fetch_tickers`, `fetch_funding_rates` |
| **Account** | `fetch_balance`, `fetch_positions`, `fetch_open_orders`, `fetch_closed_orders`, `fetch_my_trades` |
| **Trading** | `create_order`, `create_orders`, `cancel_order`, `cancel_all_orders` |
| **Analytics** | `get_delta_exposure`, `get_orderbook_analytics` |

### Safety

- **Read-only by default** — trading tools require explicit `read_only: false`
- **Sandbox by default** — prevents accidental mainnet trades
- **Symbol whitelist/blacklist** — restrict tradeable pairs via config
- **Cost caps** — inherited from ccxt-pandas order validation

## Claude Code Integration

CCXT-Pandas includes a Claude Code skill to accelerate your development workflow!

The skill provides:
- Quick reference for sync/async usage patterns
- Common DataFrame structures for all methods
- Batch operation examples and best practices
- Troubleshooting tips and testing setup

### Using the Skill

**In this repository:** The skill is automatically available. Invoke with `/ccxt-pandas-helper`

**In your projects:** Copy to your global skills directory:

```bash
# Windows
cp .claude/skills/ccxt-pandas-helper.md %USERPROFILE%\.claude\skills\

# macOS/Linux
cp .claude/skills/ccxt-pandas-helper.md ~/.claude/skills/
```

After copying, use `/ccxt-pandas-helper` in any project for instant access to ccxt-pandas patterns and documentation.

See [.claude/skills/README.md](.claude/skills/README.md) for more details.

## About Sigma Quantiphi
[Sigma Quantiphi](https://www.sigmaquantiphi.com/) is a quantitative-engineering firm that builds end-to-end algorithmic-trading systems for the cryptocurrency markets.
We create open-source, Python-first tools—like ccxt-pandas—and deliver turnkey execution, data, and research pipelines that emphasize simplicity, transparency, and rapid deployment.

## License

This project is licensed under the Apache License. See the `LICENSE` file for more details.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository, create a new branch for your feature
or fix, and send a pull request.

1. Fork the repository.
2. Create your feature/fix branch: `git checkout -b my-new-feature`.
3. Commit your changes: `git commit -am 'Add some feature'`.
4. Push to the branch: `git push origin my-new-feature`.
5. Submit a pull request.

## Support

If you encounter any issues or have questions, feel free to open an issue on
the [GitHub repository](https://github.com/yourusername/ccxt-pandas) or contact us via email at contact@sqphi.com.
Happy trading! 🚀
