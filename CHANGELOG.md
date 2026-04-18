## Unreleased

### Added
- **Explorer Dashboard** (`ccxt-pandas[explorer]`): bundled Streamlit dashboard for browsing CCXT methods. CLI: `ccxt-pandas-explorer`.
- **Custom exception hierarchy** (`CCXTPandasError`, `CCXTPandasOrderError`, `CCXTPandasSchemaError`, `CCXTPandasMethodError`). Subclasses of `ValueError` / `AttributeError` for backward compat.
- **Schemas re-exported from package root** — `from ccxt_pandas import OHLCVSchema, OrderSchema, …` now works.
- **PEP 561 typing**: `py.typed` markers in `ccxt_pandas`, `ccxt_pandas_mcp`, `ccxt_pandas_explorer`. Added `Typing :: Typed` classifier.
- **Test infrastructure**: `tests/conftest.py` with stub-credential fixtures + `mocked_responses` / `mocked_aioresponses`; hypothesis schema round-trip in `tests/test_schemas_hypothesis.py`. Live tests gated under `tests/integration/` behind `CCXT_LIVE` / `CCXT_LIVE_TRADING`.
- **CI/CD**: split CI into lint + typecheck + test jobs (Python 3.11/3.12/3.13), Codecov upload, concurrency cancellation. `publish.yml` now runs lint + tests + emits PEP 740 sigstore attestations.
- **Tooling**: ruff (lint+format), mypy (with per-module overrides for generated stubs), pre-commit hooks (ruff, ruff-format, trailing-whitespace, end-of-file-fixer, check-yaml, detect-secrets), dependabot (pip + GH Actions weekly with grouped PRs).
- **MCP**: `CCXT_MCP_MAX_ROWS` env var (default 100) for output truncation; safety defaults surfaced in `FastMCP.instructions`.
- **Governance**: `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `STABILITY.md`, `.env.example`, `.claudeignore`, PR template, 3 issue templates.
- **New examples**: `12_options_strategy_around_event.py`, `18_cheapest_withdrawal_route.py`, `19_multi_exchange_greeks.py`, `20_caching_repeat_fetches.py` (ported from newsletter repo).
- **Documentation site moved from ReadTheDocs to GitHub Pages**: `https://sigma-quantiphi.github.io/ccxt-pandas/`. Sphinx + furo + MyST (Markdown). New guides: `getting-started`, `dataframes`, `explorer`, `mcp-server`. Built and deployed by `.github/workflows/docs.yml`. The old ReadTheDocs project can be archived on the RTD dashboard.
- **Jupyter notebooks for 17 examples** paired with the `.py` sources via `jupytext` (config in `examples/jupytext.toml`). Binder installs from `binder/requirements.txt` (Python 3.13). The 4 async / WebSocket examples (`10`, `14`, `16`, `17`) stay `.py`-only because `asyncio.run()` and infinite WS loops don't work inside Jupyter's existing event loop. Pre-commit hook keeps the two formats in sync.
- **MCP server expansion: 21 → 72 tools across 7 categories** ([plan](.claude/plan/how-complete-is-our-declarative-ullman.md)).
  - Phase 1 — usability: `safe_tool` decorator wraps every tool so ccxt errors render as `Error: rate limited by exchange. …` instead of raw tracebacks; `to_list` accepts comma-separated symbol params; `resolve_max_rows` adds `max_rows=0` → unlimited; new `list_configured_accounts` tool mirrors the `accounts://list` resource.
  - Phase 2 — read coverage: 30 new fetch tools across `market_data` (bids_asks, mark/last prices, funding rate/history/intervals, open interest current/history/many, long-short ratio history, liquidations, volatility history, option chain, all greeks) and `account` (single fetch_order/fetch_position, fetch_orders/canceled/closed-and-canceled, positions history, leverages, leverage tiers, trading/transaction fees, deposit addresses, deposits, withdrawals, ledger, borrow interest, cross/isolated borrow rate, transfers, accounts, fetch_status).
  - Phase 3 — write expansion: 7 new write tools — `edit_order`, `edit_orders`, `set_leverage`, `set_margin_mode`, `set_position_mode`, `transfer`, and `withdraw` (double-gated behind `read_only=False` AND `allow_withdrawals=True`, optional `withdraw_address_allowlist`).
  - Phase 4 — implicit-method dispatcher: `call_exchange_method(method_name, params_json, …)` covers all ~140 exchange-specific endpoints in `ccxt_pandas/wrappers/exchange_parsers.py` (Binance Earn / algo, OKX Rubik / margin / lending). Discovery via new resources `implicit-methods://list` and `implicit-methods://<exchange>`. `MethodConfig` gains an `is_write: bool` field for data-driven write classification; the dispatcher also falls back to a name-pattern heuristic.
  - Phase 5 — OKX grid as featured surface: 5 read tools (`okx_grid_pending`, `_history`, `_details`, `_sub_orders`, `_positions`) and 3 write tools (`okx_grid_create`, `_stop`, `_modify`), all with named parameters. Added 6 OKX grid `privatePost*` configs to `OKX_METHOD_CONFIG` with `is_write=True`.
  - Tests: `tests/test_mcp_server.py` covers the helper utilities, gate functions, write-heuristic, server registration, and parser registry (16 tests).

### Changed
- Order-preprocessing raises now use `CCXTPandasOrderError` (subclass of `ValueError`, so existing `except ValueError:` blocks keep working).

### Examples
- **Examples**: Reintroduced `examples/` directory with 17 runnable scripts (ported from crypto-pandas-tutorials):
  - Market data & analysis: spot/future/swap spreads, exchange arbitrage, orderbook VWAPs, trade/depth plotting, coin-quoted pricing, volatility history, open interest
  - Account & trading: private data fetch, market making orders, deposits/withdrawals, delta position calculation
  - WebSocket streaming: liquidation events, order placement via WebSocket
  - Async bulk operations: 1000-symbol OHLCV loading, all-exchange market loading
  - All imports updated from `crypto_pandas` to `ccxt_pandas`
- **MCP Server** (`ccxt-pandas[mcp]`): Model Context Protocol server exposing ccxt-pandas as AI-assistant tools
  - 20 tools across 5 categories: exchange info, market data, account, trading, calculations
  - MCP resources: `exchanges://list`, `accounts://list`
  - Built on FastMCP v3 with async-only architecture
  - Read-only + sandbox mode by default for safety
  - Symbol whitelist/blacklist and cost cap enforcement
  - Config via JSON file (`CCXT_MCP_CONFIG`) or env vars (`CCXT_MCP_ACCOUNT_<name>_*`)
  - CLI entry point: `ccxt-pandas-mcp`
  - Compatible with Claude Desktop, Claude Code, and other MCP clients
- **Claude Code Skill**: Added `.claude/skills/ccxt-pandas-helper.md` skill for accelerated development with Claude Code
  - Quick reference for sync/async usage patterns
  - Common DataFrame structures for all methods
  - Batch operation examples and best practices
  - Troubleshooting tips and testing setup
  - Copy to `~/.claude/skills/` to use in any project
- **Pandera Schemas**: Comprehensive schema definitions for all DataFrame types (35+ schemas)
  - Located in `ccxt_pandas/wrappers/schemas/`
  - Documents DataFrame structures for all fetch methods
  - Includes schemas for: OHLCV, orders, trades, positions, balances, tickers, and more
  - `FeeFieldsMixin` for consistent fee field handling across schemas
  - Schemas use data-driven approach based on real exchange responses
  - **New schemas**: `LedgerSchema`, `AddressesSchema`, `MarginsBalanceSchema`
- **Schema Validation Integration** (opt-in):
  - Added `validate_schemas` parameter to `CCXTPandasExchange` and `AsyncCCXTPandasExchange` (default: `False`)
  - Added `strict_validation` parameter for fail-fast vs. warning-only validation (default: `False`)
  - Automatic schema mapping for 60+ methods via `method_mappings.get_method_schema()`
  - Validation occurs after DataFrame conversion in `BaseProcessor`
  - Lazy loading with caching to avoid circular dependencies
- **Pandera Type Hints**:
  - Type stubs now use `DataFrame[SchemaName]` from `pandera.typing`
  - IDE autocomplete shows expected DataFrame structure for all methods
  - Example: `fetch_balance() -> DataFrame[BalanceSchema]`
  - Auto-imports Pandera schemas in generated type stubs
  - Regenerate with: `uv run python ccxt_pandas/utils/_generate_typed_interface.py`
- **Order Book Analysis Functions** (9 new functions in `ccxt_pandas.calculations.orderbook`):
  - `calculate_vwap_by_depth()`: VWAP at various notional depths with partial fill support
  - `calculate_mid_price()`: Average of best bid/ask
  - `calculate_spread()`: Absolute or relative bid-ask spread
  - `sort_orderbook()`: Sort by symbol, side, and price (best prices first)
  - `calculate_notional()`: Price × quantity
  - `signed_price()`: Signed prices for sorting (+1 asks, -1 bids)
  - `side_sign()`: Directional sign for order book sides
  - `is_ask_side()`: Identify ask/sell rows (handles both formats)
  - `create_mirrored_sides()`: Create symmetric order book sides for testing
  - All functions support both `'asks'/'bids'` and `'buy'/'sell'` formats
- **Calculations Module Enhancements**:
  - Moved `floor_series()` and `ceil_series()` to `ccxt_pandas.calculations.precision`
  - All trade analysis functions now use `@pa.check_types` for automatic Pandera validation
  - `calculate_delta_exposure()` now supports both `BalanceSchema` and `MarginsBalanceSchema`

### Changed
- Updated `.gitignore` to allow `.claude/skills/` directory while ignoring other Claude Code local files
- **Breaking**: Split `BalanceSchema` into two schemas:
  - `BalanceSchema`: For spot balances (uses `code` field)
  - `MarginsBalanceSchema`: For margin balances (uses `symbol` field with `base_*` and `quote_*` columns)
- Replaced manual DataFrame validation with `@pa.check_types` decorator in calculations module
- Made `side`, `baseValue`, and `quoteValue` optional in `LiquidationsSchema`

### Documentation
- Added MCP Server section to README.md with installation, configuration, and usage guide
- Added MCP Server architecture section to CLAUDE.md
- Updated README.md examples section to reference local `examples/` directory
- Updated `docs/source/examples.rst` to reference local examples
- Added Claude Code Integration section to README.md
- Added Claude Code Skill section to CLAUDE.md
- Created `.claude/skills/README.md` with usage instructions
- Added comprehensive order book analysis documentation in `ccxt_pandas/calculations/README.md`
- All orderbook functions include detailed docstrings with examples and use cases

## v0.13.0
- Renaming project to `CCXT-Pandas` for clearer link between Pandas & CCXT.

## v0.12.7
- Addressed Pandera import issue.

## v0.12.6
- Added new methods such as `fetchFundingIntervals` and `fetchOptionChain`.

## v0.12.5
- Fixed order to dataframe by adding optional `attach_trades_to_orders` argument.

## v0.12.4
- Changed `market_to_dataframe` parsing to use `pd.DataFrame.from_dict`.

## v0.12.3
- Introduced `has_method` method.

## v0.12.1
- Replaced Na values inside of markets limits with 0 for min and np.inf for max.

## v0.12.0
- Breaking Change: Replaced `notional` argument when sending orders with `cost` to align with CCXT.
- Added checks for order cost within bounds.

## v0.11.9
- Fix `orders_to_dict` should there be no price column.
- Added order create, cancel, edit methods that use websockets.

## v0.11.8
- Fixed order preprocessing for orders out of bounds.

## v0.11.7
- Added `fetch_my_dust_trades`, `fetch_portfolios`, `fetch_portfolio_details`, `fetch_accounts`.

## v0.11.6
- Added `fetch_orders_by_ids`, `fetch_orders_by_status`.

## v0.11.5
- Added multiple watch methods parsing: balance, my_liquidations, funding_rate.

## v0.11.4
- Added `lastTradeTimestamp` and `lastUpdateTimestamp` to datetime columns.

## v0.11.2
- Forward `close` as well into `AsyncCCXTPandasExchange`.

## v0.11.1
- Added `fetch_deposits_withdrawals`, `fetch_order_trades` and `fetch_volatility_history` methods.

## v0.11.0
- Refactored `preprocess_data` as method of CCXTProcessor and not CCXTPandasExchange.
- Introduced a type-hinting generator and used the created classes to introduce type-hinting.

## v0.10.4
- Migrated `fetch_deposit_withdraw_fees` to `currencies` format.

## v0.10.3
- Separate dataframe format for `fetch_currencies`.
- Switched `fetched_leverages` from standard to markets dataframe format.

## v0.10.2
- Improved performance by dropping Na before type conversion.

## v0.10.1
- Quick fix dict values params `|` changed to `or`

## v0.10.0
- Delegated price/amount rounding to ccxt.exchange.price_to_precision/amount_to_precision .
- Removal of price/amount rounding strategy.

## v0.9.32
- Remove error message on missing `amount` orders. Allows compatible with params={"cost": value}.
- Created fix using `reindex` should precision/ limit fields not exist in markets data.

## v0.9.32
- Enabled cost -> amount calculation for market orders.
- Created fix using `reindex` should precision/ limit fields not exist in markets data.

## v0.9.31
- Only adding `timestamp` and `datetime` fields to balance dataframe when present in dict.
- Only parsing numeric/bool/datetime fields if list non empty.

## v0.9.29
- Added `nextFundingDatetime` to datetime parsing.

## v0.9.28
- Only concat non empty orderbooks.

## v0.9.27
- Added `fundingRate` and `estimatedSettlePrice` to numeric fields.
- Introduced `dropna_fields` with default True to automatically remove all Na columns. 

## v0.9.26
- Addition of `fetch_cross_borrow_rate(s)` parsing.

## v0.9.25
- Addition of `fetch_all_greeks` parsing.

## v0.9.24
- Addition of `fetch_funding_rate` parsing.

## v0.9.23
- Add `return_exceptions` to lists of lists in async_concat_results.

## v0.9.22
- Print warnings for out of bounds orders only if dataframe not empty.
- Extract exchange name from exchange class if not provided.
- Certain tests reverted to prod Binance exchange.

## v0.9.20
- Added fields to numeric and numeric_datetime columns for parsing: fee, expiryDate, createdDate.

## v0.9.19
- Added parsing for `fetchLastPrices`, `fetchIsolatedBorrowRates` and `fetchIsolatedBorrowRate`.

## v0.9.18
- Added parsing for `fetchMarkets`, `fetchMarkPrices` and `fetchMarkPrice`.

## v0.9.15
- Added `price_out_of_range` and `volume_out_of_range` parameters to allow user
to determine if they want a warning when price/volume out of limits range or if they want the values to be clipped.

## v0.9.14
- Clipping `price` and `amount` only if min/max values are not null from `load_markets`.

## v0.9.11
- Added DataFrame parsing for `fetch_order_books`.

## v0.9.7
- Fix to `account` column name.

## v0.9.6
- `async_concat_results` can now accept awaitable, listvawaitable or listvlistvawaitable

## v0.9.5
- Introduced `account` and `exchange` parameters in BaseProcessor for CCXT-Pandas-Pro.
- Made `BaseProcessor` attribute of CCXTPandasExchange.

## v0.9.1
- Created asyncio `concat_gather_results` function.

## v0.9.0
- New architecture with simple method inheritance.
- Fixed `watchOHLCVForSymbols` data parsing.
- Fixed `ohlcv` snake/camel case mapping.
- Reintroduced semaphore.

## v0.8.0c
- Remove OHLCV symbol column. Async reroutes non async compatible methods.

## v0.8.0b
- Add `fundingHistory` data parsing

## v0.8.0a
- Both sync and async methods with getattr for simpler architecture and future method additions.
- Async create/edit/cancel orders now possible.

## v0.7.12
- Added fix should params column be provided.

## v0.7.11
- Fix to `fetch_funding_rates` dataframe output.

## v0.7.9
- Introduced `fetch_trading_fee` and `fetch_trading_fees`.

## v0.7.7
- Fix to rounding should `precision` or `limits` not be present in order creation/ editing.

## v0.7.5
- Keep None since.

## v0.7.4
- `since` can now be a str of pdTimedelta
e.g: `"7d"` to set 7 days ago.

## v0.7.2
- `since` can now be a dict of pd.DateOffset parameters
e.g: `{"days": -1, "hour": 0, "minute": 0, "seconds": 0}` to set  to yesterday midnight.

## v0.7.0
- Use underscore rather than dot for unpacking dict columns.

## v0.6.3
- Added balance parsing for isolated margins.

## v0.6.2
- Append `symbol` column to OHLCV to facilitate multi symbols.

## v0.6.0
- Both CCXTPandasExchange and AsyncCCXTPandasExchange no longer inherit from CCXT Exchange.

## v0.5.2
- Fixed `fetch_funding_history` API call in both sync and async class.

## v0.5.0
- Transformed `orders_dataframe_preprocessing` into standard function to allow simpler use within ccxt-pandas-pro.

## v0.4.11
- Adding default `WindowsSelectorEventLoopPolicy` to `AsyncCCXTPandasExchange`.

## v0.4.10
- Added `fetch_funding_history` method.

## v0.4.5
- Set default errors to ignore.

## v0.4.0
- Introduced `CCXTPandasExchange` and `AsyncCCXTPandasExchange` to enable working with
`Pandas` in one line of code.

## v0.2.0
- New architecture around classes for Preprocessors.

## v0.1.20
- Added `market_to_dataframe()`

## v0.1.0

- Initial deploy