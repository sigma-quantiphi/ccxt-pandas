"""Exchange info tools — list exchanges/accounts, load_markets, currencies, status."""

from __future__ import annotations

import json
from typing import Literal

import ccxt
from fastmcp import Context, FastMCP

from ccxt_pandas_mcp._helpers import safe_tool
from ccxt_pandas_mcp.exchange_manager import ExchangeManager
from ccxt_pandas_mcp.serialization import serialize_dataframe


def register_exchange_info_tools(mcp: FastMCP):
    @mcp.tool()
    @safe_tool
    async def list_exchanges() -> str:
        """List every cryptocurrency exchange supported by CCXT (one per line)."""
        return "\n".join(ccxt.exchanges)

    @mcp.tool()
    @safe_tool
    async def list_configured_accounts(ctx: Context = None) -> str:
        """List the exchange accounts configured on this server.

        Mirrors the `accounts://list` resource as a tool so Claude finds it via
        tool-search. Returns a JSON object keyed by account name.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        out = {}
        for name in manager.account_names:
            ex = manager.get_exchange(name)
            out[name] = {
                "exchange": ex.exchange.id,
                "sandbox": getattr(ex.exchange, "sandbox", False),
            }
        return json.dumps(out, indent=2)

    @mcp.tool()
    @safe_tool
    async def load_markets(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 200,
        ctx: Context = None,
    ) -> str:
        """Load every trading pair / market for an exchange.

        Returns:
            DataFrame columns include: `symbol`, `base`, `quote`, `settle`,
            `type`, `subType`, `active`, `precision_*`, `limits_*_min`,
            `limits_*_max`, `contractSize`, `expiryDatetime`, `strike`,
            `optionType`. One row per symbol.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.load_markets()
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)

    @mcp.tool()
    @safe_tool
    async def fetch_currencies(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 200,
        ctx: Context = None,
    ) -> str:
        """Fetch every currency supported by an exchange.

        Returns:
            DataFrame: `id`, `code`, `name`, `precision`, `withdraw`, `deposit`,
            `network`, `network_id`, `network_fee`, `exchange`. One row per
            `(currency, network)` combination — networks are exploded.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.fetch_currencies()
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)

    @mcp.tool()
    @safe_tool
    async def fetch_status(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch the exchange's operational status (`ok`, `shutdown`, `maintenance`).

        Returns:
            DataFrame: `status`, `updated`, `eta`, `url`, `info`.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.fetch_status()
        return serialize_dataframe(df, fmt=output_format)
