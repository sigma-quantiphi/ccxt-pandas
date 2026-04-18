"""ccxt-pandas exception hierarchy.

All errors raised inside ccxt-pandas inherit from `CCXTPandasError`. Specific
subclasses also inherit from the relevant builtin (`ValueError`,
`AttributeError`) so existing `except ValueError:` blocks keep working.

ccxt's own exceptions (`AuthenticationError`, `RateLimitExceeded`,
`NetworkError`, etc.) propagate unchanged.
"""

from __future__ import annotations


class CCXTPandasError(Exception):
    """Base exception for all ccxt-pandas errors."""


class CCXTPandasOrderError(CCXTPandasError, ValueError):
    """Raised when order preprocessing or validation fails (limits, price, schema)."""


class CCXTPandasSchemaError(CCXTPandasError, ValueError):
    """Raised when a response fails pandera schema validation."""


class CCXTPandasMethodError(CCXTPandasError, AttributeError):
    """Raised when an unsupported method is requested via `__getattribute__`."""
