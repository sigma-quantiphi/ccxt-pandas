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
Find all examples in the [CCXT-Pandas-Example Repository](https://github.com/sigma-quantiphi/ccxt-pandas-examples)

## Getting Started

CCXT-Pandas works identically to CCXT. Just add `exchange = CCXTPandasExchange(exchange=exchange)`
and the exchange methods provided by CCXT will be exposed to CCXT-Pandas.
More examples can be found on [Binder](https://mybinder.org/v2/gh/sigma-quantiphi/ccxt-pandas/HEAD?urlpath=%2Fdoc%2Ftree%2Fexamples): 

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
