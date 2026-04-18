"""DataFrame serialization for MCP responses."""

from __future__ import annotations

import os
from typing import Literal

import pandas as pd

DEFAULT_MAX_ROWS = int(os.getenv("CCXT_MCP_MAX_ROWS", "100"))
UNLIMITED_ROWS = 999_999


def resolve_max_rows(max_rows: int | None) -> int:
    """Resolve `max_rows` parameter against env default + sentinel.

    - `None` → `CCXT_MCP_MAX_ROWS` env var (default 100)
    - `0` → unlimited (999_999)
    - any positive int → use as-is
    """
    if max_rows is None:
        return DEFAULT_MAX_ROWS
    if max_rows == 0:
        return UNLIMITED_ROWS
    return max_rows


def serialize_dataframe(
    df: pd.DataFrame,
    fmt: Literal["markdown", "json", "csv"] = "markdown",
    max_rows: int | None = None,
) -> str:
    """Serialize a DataFrame to a string suitable for MCP tool responses.

    Args:
        df: The DataFrame to serialize.
        fmt: Output format — "markdown" (default), "json", or "csv".
        max_rows: Maximum rows to include. Defaults to `CCXT_MCP_MAX_ROWS`
            env var (or 100). Pass 0 for unlimited. Excess rows are noted in
            the output.
    """
    effective_max = resolve_max_rows(max_rows)

    total = len(df)
    truncated = total > effective_max
    if truncated:
        df = df.head(effective_max)

    if fmt == "json":
        result = df.to_json(orient="records", date_format="iso", indent=2)
    elif fmt == "csv":
        result = df.to_csv(index=False)
    else:
        result = df.to_markdown(index=False)

    if truncated:
        result += (
            f"\n\n... showing {effective_max} of {total} rows. "
            f"Pass `max_rows=0` for all rows or `max_rows=<N>` for a custom cap."
        )

    return result
