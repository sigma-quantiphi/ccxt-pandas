---
name: regenerate-typed-stubs
description: Regenerate the auto-generated Protocol type stubs at ccxt_pandas/utils/ccxt_pandas_exchange_typed.py and async_ccxt_pandas_exchange_typed.py. Use whenever CCXT methods are added/renamed/removed upstream, or when ccxt is bumped to a new version.
---

# Regenerate typed stubs

The Protocol classes that drive IDE autocomplete on `CCXTPandasExchange` and
`AsyncCCXTPandasExchange` are generated from CCXT's introspectable surface.
After bumping the `ccxt` dependency or adding new methods to
`method_mappings.py`, regenerate them:

```bash
uv run python ccxt_pandas/utils/_generate_typed_interface.py
```

This rewrites:

- `ccxt_pandas/utils/ccxt_pandas_exchange_typed.py`
- `ccxt_pandas/utils/async_ccxt_pandas_exchange_typed.py`

These files are excluded from ruff lint and mypy via per-file ignores in
`pyproject.toml`, so the diff should not introduce new lint/type failures.

## Verify

```bash
uv run ruff format ccxt_pandas/utils/  # leaves the _typed.py files untouched but formats neighbors
uv run python -c "from ccxt_pandas import CCXTPandasExchange, AsyncCCXTPandasExchange"
uv run pytest tests/ -v
```

## Commit

Use a dedicated commit so the diff is easy to review and revert:

```
Regenerate typed stubs against ccxt vX.Y.Z
```

If the regeneration was triggered by a `ccxt` version bump, include the
`ccxt` change in the same commit.
