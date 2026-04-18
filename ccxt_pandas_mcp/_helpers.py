"""Shared helpers for MCP tools.

`safe_tool` decorates async tool functions to convert exchange exceptions into
human-readable strings instead of raw tracebacks. `to_list` parses
comma-separated strings into Python lists for symbol/code params (Claude often
finds string-of-list easier than JSON).
"""

from __future__ import annotations

import functools
from collections.abc import Awaitable, Callable
from typing import TypeVar

import ccxt

from ccxt_pandas import (
    CCXTPandasError,
    CCXTPandasMethodError,
    CCXTPandasOrderError,
    CCXTPandasSchemaError,
)

F = TypeVar("F", bound=Callable[..., Awaitable[str]])


def safe_tool(fn: F) -> F:
    """Decorator: catch exchange/library exceptions and return a string.

    Order matters: place between `@mcp.tool()` (outer) and the function (inner):

        @mcp.tool()
        @safe_tool
        async def my_tool(...) -> str: ...
    """

    @functools.wraps(fn)
    async def wrapper(*args, **kwargs) -> str:
        try:
            return await fn(*args, **kwargs)
        except ccxt.AuthenticationError as e:
            return f"Error: authentication failed. Check API credentials for this account. ({e})"
        except ccxt.RateLimitExceeded as e:
            return f"Error: rate limited by exchange. Wait and retry. ({e})"
        except ccxt.ExchangeNotAvailable as e:
            return f"Error: exchange unavailable or in maintenance. ({e})"
        except ccxt.BadSymbol as e:
            return f"Error: invalid or unsupported symbol. ({e})"
        except ccxt.InvalidOrder as e:
            return f"Error: invalid order parameters. ({e})"
        except ccxt.InsufficientFunds as e:
            return f"Error: insufficient funds for this order. ({e})"
        except ccxt.NetworkError as e:
            return f"Error: network failure talking to exchange. ({e})"
        except (CCXTPandasOrderError, CCXTPandasSchemaError, CCXTPandasMethodError) as e:
            return f"Error ({type(e).__name__}): {e}"
        except CCXTPandasError as e:
            return f"Error: {e}"
        except PermissionError as e:
            return f"Error: {e}"
        except ccxt.ExchangeError as e:
            return f"Error: exchange returned an error. {type(e).__name__}: {e}"
        except Exception as e:
            return f"Error: {type(e).__name__}: {e}"

    return wrapper  # type: ignore[return-value]


def to_list(val: str | list[str] | None) -> list[str] | None:
    """Coerce a comma-separated string or list into a list of stripped strings.

    Claude often passes "BTC/USDT,ETH/USDT" as one string. This accepts both
    forms and returns None when there's nothing to use.
    """
    if val is None:
        return None
    if isinstance(val, list):
        return val or None
    parts = [s.strip() for s in str(val).split(",") if s.strip()]
    return parts or None
