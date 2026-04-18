# Contributing to ccxt-pandas

Thanks for your interest in contributing!

## Development Setup

```bash
git clone https://github.com/sigma-quantiphi/ccxt-pandas.git
cd ccxt-pandas
uv sync --extra dev --extra mcp --extra explorer
```

## Running Checks

```bash
uv run ruff check .                       # lint
uv run ruff format --check .              # format check
uv run mypy ccxt_pandas                   # type check
uv run pytest tests/                      # unit tests (no API keys needed)
CCXT_LIVE=1 uv run pytest tests/integration/  # live read-only tests
CCXT_LIVE_TRADING=1 uv run pytest tests/integration/  # live order-lifecycle tests
```

The default `pytest tests/` collection skips `tests/integration/` entirely — no live API calls happen unless you set `CCXT_LIVE` or `CCXT_LIVE_TRADING`. Live integration tests require API keys in `.env` (see `.env.example`).

## Adding a New CCXT Method

1. Decide its response category in `ccxt_pandas/wrappers/method_mappings.py` (standard / markets / currencies / balance / OHLCV / orderbook / orders / dict).
2. Add a Pandera schema under `ccxt_pandas/wrappers/schemas/`.
3. If the method introduces new field types, register them in `ccxt_pandas/wrappers/field_type_mappings.py`.
4. Regenerate the typed stubs: `uv run python ccxt_pandas/utils/_generate_typed_interface.py`.
5. Add a unit test (mock the HTTP layer with `responses` / `aioresponses`).
6. Update `CHANGELOG.md` under `[Unreleased]`.

## Pull Requests

1. Fork the repo and create a feature branch from `main`.
2. Add tests for new functionality.
3. Ensure `ruff`, `mypy`, and `pytest tests/` all pass.
4. Open a PR with a clear description of the change.

## Reporting Issues

Open an issue at https://github.com/sigma-quantiphi/ccxt-pandas/issues with:
- What you expected vs what happened
- Minimal reproduction steps
- Python version, ccxt version, and `ccxt-pandas` version
- Which exchange the call is targeting (responses vary by exchange)
