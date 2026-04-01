"""Exchange info tools — load_markets, fetch_currencies, list exchanges."""

from __future__ import annotations

from typing import Literal

import ccxt
from fastmcp import Context, FastMCP

from ccxt_pandas_mcp.exchange_manager import ExchangeManager
from ccxt_pandas_mcp.serialization import serialize_dataframe


def register_exchange_info_tools(mcp: FastMCP):

    @mcp.tool()
    async def list_exchanges() -> str:
        """List all cryptocurrency exchanges supported by CCXT."""
        return "\n".join(ccxt.exchanges)

    @mcp.tool()
    async def load_markets(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int = 200,
        ctx: Context = None,
    ) -> str:
        """Load all trading pairs/markets for an exchange.

        Returns a DataFrame with columns: symbol, base, quote, type, active,
        and detailed market specifications (limits, precision, fees).
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.load_markets()
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)

    @mcp.tool()
    async def fetch_currencies(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int = 200,
        ctx: Context = None,
    ) -> str:
        """Fetch all currencies supported by an exchange.

        Returns currency info including deposit/withdrawal networks and fees.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.fetch_currencies()
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)
