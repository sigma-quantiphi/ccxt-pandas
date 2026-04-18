"""DataFrame serialization for MCP responses."""

from __future__ import annotations

import os
from typing import Literal

import pandas as pd

DEFAULT_MAX_ROWS = int(os.getenv("CCXT_MCP_MAX_ROWS", "100"))


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
            env var (or 100). Excess rows are noted in the output.
    """
    if max_rows is None:
        max_rows = DEFAULT_MAX_ROWS

    total = len(df)
    truncated = total > max_rows
    if truncated:
        df = df.head(max_rows)

    if fmt == "json":
        result = df.to_json(orient="records", date_format="iso", indent=2)
    elif fmt == "csv":
        result = df.to_csv(index=False)
    else:
        result = df.to_markdown(index=False)

    if truncated:
        result += f"\n\n... showing {max_rows} of {total} rows. Use `limit` to fetch more."

    return result
