# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

ccxt-pandas is a Python library that wraps [CCXT](https://github.com/ccxt/ccxt/) exchange methods so they return pandas DataFrames instead of raw JSON/dicts. It supports both synchronous and asynchronous usage, including WebSocket streams via `ccxt.pro`.

## Build & Development

- **Build system**: UV with hatchling backend
- **Python**: >= 3.11
- **Install dependencies**: `uv sync`
- **Install with docs deps**: `uv sync --extra docs`
- **Install with dev deps**: `uv sync --group dev`
- **Install everything**: `uv sync --all-extras --all-groups`

## Running Tests

Tests require live exchange API keys configured in a `.env` file (see `.env` for the expected variables: `SANDBOX_API_KEY`, `SANDBOX_API_SECRET`, `API_KEY`, `API_SECRET`, `OKX_API_KEY`, `OKX_API_SECRET`, `OKX_API_PASSWORD`, `COINBASE_API_KEY`, `COINBASE_API_SECRET`).

```bash
# Run all tests
uv run pytest tests/

# Run a single test
uv run pytest tests/test_sync.py::test_fetch_ohlcv -s

# Run async test (it's a script, not pytest)
uv run python tests/test_async.py
```

Tests hit live exchange APIs (sandbox where possible) so they are not hermetic.

## Code Style

- **Linter + formatter**: Ruff (`uv run ruff check .`, `uv run ruff format .`)
- **Type checker**: mypy (`uv run mypy ccxt_pandas`)
- **Pre-commit**: ruff + ruff-format + trailing-whitespace + end-of-file-fixer + check-yaml + detect-secrets (run `pre-commit install` once after cloning)

## Testing

- **Unit tests** (default): `uv run pytest tests/` — no API keys needed; the integration dir is skipped from collection.
- **Live read-only tests**: `CCXT_LIVE=1 uv run pytest tests/integration/`
- **Live order-lifecycle tests**: `CCXT_LIVE_TRADING=1 uv run pytest tests/integration/` (places real orders on sandbox)
- **Stub fixtures** in `tests/conftest.py`: `binance_unauth`, `binance_authed_stub`, `okx_authed_stub`, `mocked_responses`, `mocked_aioresponses`.

## Regenerating Typed Interfaces

The typed stubs in `ccxt_pandas/utils/ccxt_pandas_exchange_typed.py` and `async_ccxt_pandas_exchange_typed.py` are auto-generated. Regenerate them when CCXT methods change:

```bash
uv run python ccxt_pandas/utils/_generate_typed_interface.py
```

## Architecture

### Core Classes (ccxt_pandas/wrappers/)

- **`CCXTPandasExchange`** — Sync wrapper. Takes a `ccxt.Exchange` instance. Uses `__getattribute__` to intercept CCXT method calls, preprocess inputs (timestamps, order validation), call the underlying exchange, and convert responses to DataFrames via `BaseProcessor`.

- **`AsyncCCXTPandasExchange`** — Async wrapper. Same pattern but for `ccxt.pro` exchanges. Adds semaphore-based concurrency control and supports both REST (`fetch_*`) and WebSocket (`watch_*`) methods.

- **`BaseProcessor`** — Stateless-ish dataclass that handles all response-to-DataFrame conversions. Each CCXT response shape (list-of-dicts, order book, OHLCV, balance, markets, currencies) has a dedicated conversion method. Also handles type casting (timestamps → datetime, strings → numeric, booleans).

- **`method_mappings.py`** — Central registry that categorizes every supported CCXT method by its response shape (standard DataFrame, markets, currencies, balance, OHLCV, orderbook, orders, dict). This determines which `BaseProcessor` conversion method is used. All snake_case methods are automatically duplicated as camelCase via `add_camel_case_methods`.

- **`order_schema.py`** — Pandera `DataFrameModel` for validating order DataFrames before submission.

### How Method Interception Works

Both exchange wrappers override `__getattribute__`. When a method name is in `modified_methods` (the union of all method categories from `method_mappings.py`), the wrapper:
1. Converts `since` kwargs from Timestamp/string/dict to int milliseconds
2. For order methods: validates and preprocesses the order (precision, cost limits, schema validation)
3. Calls the original CCXT exchange method
4. Routes the result through `BaseProcessor.preprocess_outputs()` based on which category the method belongs to

### Utilities (ccxt_pandas/utils/)

- **`pandas_utils.py`** — DataFrame helpers: timestamp conversion, dict column expansion, order preprocessing with exchange market limits (price/amount/cost range checking with "warn" or "clip" modes), `concat_results`/`async_concat_results` for merging multiple exchange call results.

- **`_generate_typed_interface.py`** — Code generator that introspects `ccxt.Exchange` and `ccxt.pro.Exchange` to produce Protocol classes with proper type hints for IDE autocomplete. Run from repo root.

### Explorer Dashboard (ccxt_pandas_explorer/)

Optional Streamlit dashboard, installed via `pip install ccxt-pandas[explorer]`. Migrated from the standalone `ccxt-explorer` repo — same UI, now bundled with the package.

- **`app.py`** — the Streamlit app: pick an exchange, pick a fetch method, browse markets, run the call, see the resulting DataFrame, and plot it with Plotly.
- **`cli.py`** — `ccxt-pandas-explorer` console script. Spawns `streamlit run app.py` against the bundled app path so the favicon resolves regardless of CWD.
- **`favicon.png`** — bundled via `[tool.hatch.build.targets.wheel.force-include]` in `pyproject.toml`.

No auth — runs straight in the browser. Run with: `uv run ccxt-pandas-explorer` or `ccxt-pandas-explorer` after install.

### MCP Server (ccxt_pandas_mcp/)

Optional MCP server package, installed via `pip install ccxt-pandas[mcp]`. Uses FastMCP v3.

- **`server.py`** — FastMCP entry point. Registers all tools/resources, wires up lifespan.
- **`config.py`** — Pydantic models: `MCPServerConfig`, `ExchangeAccountConfig`. Loads from JSON file (`CCXT_MCP_CONFIG` env var) or individual env vars (`CCXT_MCP_ACCOUNT_<name>_EXCHANGE`, etc.).
- **`exchange_manager.py`** — Manages `AsyncCCXTPandasExchange` instances. Initialized in FastMCP lifespan, calls `load_markets()` at startup, closes connections on shutdown.
- **`serialization.py`** — DataFrame → string conversion (markdown/json/csv) with row limiting.
- **`tools/`** — Tool modules: `exchange_info.py`, `market_data.py`, `account.py`, `trading.py`, `calculations.py`. Each exports a `register_*_tools(mcp)` function.
- **`resources/`** — MCP resources: `exchanges://list`, `accounts://list`.

**Key design**: Async-only (MCP servers are async), read-only + sandbox by default, DataFrame responses as markdown tables.

Run with: `uv run ccxt-pandas-mcp` or `ccxt-pandas-mcp` after install.

### Public API

```python
from ccxt_pandas import CCXTPandasExchange, AsyncCCXTPandasExchange
```

These are the only two public exports.

## Claude Code Skill

A helper skill is available at `.claude/skills/ccxt-pandas-helper.md` that provides:
- Quick reference for sync/async usage patterns
- Common DataFrame structures for all fetch methods
- Batch operation examples (create/cancel/edit orders)
- Best practices for rate limiting, testing, and error handling
- Troubleshooting common issues

**Usage:** Invoke with `/ccxt-pandas-helper` when working in this repository, or copy to `~/.claude/skills/` to use in other projects.

This skill is particularly useful when:
- Starting a new project that uses ccxt-pandas
- Helping other developers understand ccxt-pandas patterns
- Debugging common issues or looking up DataFrame structures
- Setting up batch operations or async workflows

## Planning

When creating or updating a plan, always save it to `.claude/plan/plan.md`. This ensures the plan persists across sessions and can be referenced later.
