# Stability & Deprecation Policy

`ccxt-pandas` follows [Semantic Versioning](https://semver.org/).

## What counts as a breaking change

Anything that can break working user code:

- Removing or renaming a public class, method, function, or parameter.
- Changing the return type of a public method (including DataFrame column names / dtypes enforced by Pandera schemas).
- Tightening a Pandera schema in a way that rejects previously-accepted input.
- Removing a re-export from the top-level package.

Anything prefixed with `_` is private and may change at any time.

## Auto-generated typed stubs

The Protocol classes in `ccxt_pandas/utils/ccxt_pandas_exchange_typed.py` and
`async_ccxt_pandas_exchange_typed.py` are regenerated from the upstream CCXT
surface. When CCXT adds, renames, or removes a method, these stubs change to
match — that is **not** treated as a `ccxt-pandas` breaking change. Pin
both `ccxt` and `ccxt-pandas` if you depend on a specific method signature.

## Deprecation window

Deprecations are announced at least **one minor release** before removal:

1. The symbol is marked with `@typing_extensions.deprecated(...)`, which raises `DeprecationWarning` at call time and is surfaced by IDEs.
2. `CHANGELOG.md` lists it under "Deprecated" with the target removal version.

Example:

```python
from typing_extensions import deprecated

@deprecated("Use `fetch_ohlcv(..., from_date=...)` instead. Removed in 0.20.0.")
def fetch_ohlcv_since(self, since): ...
```

## Upstream CCXT drift

CCXT evolves rapidly; exchange-specific quirks shift constantly. A change in
CCXT's response shape does not automatically bump `ccxt-pandas` major version
— only package-level API changes (method signatures, exposed DataFrame
columns, exported symbols) do. When upstream drift requires a parser fix,
that lands as a minor release with a `CHANGELOG.md` note.
