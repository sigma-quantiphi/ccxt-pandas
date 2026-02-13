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

- **Formatter**: Black
- **Pre-commit hook**: `detect-secrets` for preventing secret leaks

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

### Public API

```python
from ccxt_pandas import CCXTPandasExchange, AsyncCCXTPandasExchange
```

These are the only two public exports.

## Planning

When creating or updating a plan, always save it to `.claude/plan/plan.md`. This ensures the plan persists across sessions and can be referenced later.
