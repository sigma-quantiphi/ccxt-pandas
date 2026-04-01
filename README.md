# CCXT-Pandas

![Python version](https://img.shields.io/badge/python-3.11%20%7C%203.12%20%7C%203.13-blue.svg)
[![GitHub](https://img.shields.io/badge/github-Visit&nbsp;Repo-black?style=for-the-badge&logo=github)](https://github.com/sigma-quantiphi/ccxt-pandas)
[![PyPI version](https://badge.fury.io/py/ccxt-pandas.svg)](https://pypi.org/project/ccxt-pandas/)
[![Downloads](https://static.pepy.tech/personalized-badge/ccxt-pandas?period=month&units=international_system&left_color=grey&right_color=blue&left_text=downloads/month)](https://pepy.tech/project/ccxt-pandas)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/sigma-quantiphi/ccxt-pandas/HEAD?urlpath=%2Fdoc%2Ftree%2Fexamples)
[![Explore Data](https://img.shields.io/badge/Explore%20Data-CCXT--Explorer-ffffff?logo=streamlit&style=plastic&color=ffffff&logoColor=FF4B4B)](https://www.ccxt-explorer.com/)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/sigma-quantiphi/ccxt-pandas/blob/main/LICENSE.md)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Docs](https://readthedocs.org/projects/ccxt-pandas/badge/?version=latest)](https://ccxt-pandas.readthedocs.io/en/latest/)
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

See the [`examples/`](examples/) directory for 17 runnable scripts covering market data, trading, analytics, and WebSocket streaming:

| # | Script | Description | Auth? |
|---|--------|-------------|-------|
| 01 | [Spot/Future/Swap Analysis](examples/01_spot_future_swap_price_volume_analysis.py) | BTC spread and volume across contract types | No |
| 02 | [Exchange Arbitrage](examples/02_exchange_arbitrage.py) | Cross-exchange spread detection | No |
| 03 | [Fetch Private Data](examples/03_fetch_private_data.py) | Trades, positions, greeks | Yes |
| 04 | [Plot Trades](examples/04_plot_trades.py) | OHLCV candlestick + trade scatter charts | No |
| 05 | [Orderbook Depth](examples/05_plot_orderbook_depth.py) | Cumulative depth chart | No |
| 06 | [Orderbook VWAPs](examples/06_calculate_orderbook_vwaps.py) | VWAP at multiple notional depths | No |
| 07 | [Market Making](examples/07_market_making_orders.py) | LIMIT_MAKER and QUEUE orders | Yes |
| 08 | [Coin-Quoted Pricing](examples/08_pricing_coin_quoted_symbols.py) | Convert to USDT-equivalent prices | No |
| 09 | [Deposits/Withdrawals](examples/09_deposits_withdrawals.py) | Fetch deposit/withdrawal history | Yes |
| 10 | [WS Liquidations](examples/10_websockets_listen_liquidations.py) | Stream live liquidation events | No |
| 11 | [Volatility History](examples/11_fetch_volatility_history.py) | BTC volatility from Deribit | No |
| 13 | [Delta Position](examples/13_delta_position.py) | Net delta across spot + derivatives | Yes |
| 14 | [WS Orders](examples/14_send_orders_via_websockets.py) | Place/edit orders via WebSocket | Yes |
| 15 | [Open Interest](examples/15_open_interest_history.py) | Historical open interest + pct change | No |
| 16 | [1000 OHLCV Async](examples/16_load_1000_ohlcv_async.py) | Bulk OHLCV with `asyncio.gather` | No |
| 17 | [All Exchanges Async](examples/17_load_symbols_all_exchanges_async.py) | Load markets from every exchange | No |

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
