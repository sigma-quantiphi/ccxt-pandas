"""MCP resources — exchange lists, account info."""

from __future__ import annotations

import json

import ccxt
from fastmcp import Context, FastMCP

from ccxt_pandas_mcp.exchange_manager import ExchangeManager


def register_resources(mcp: FastMCP):

    @mcp.resource("exchanges://list")
    async def list_exchanges() -> str:
        """List all cryptocurrency exchanges supported by CCXT."""
        return json.dumps(ccxt.exchanges, indent=2)

    @mcp.resource("accounts://list")
    async def list_accounts(ctx: Context) -> str:
        """List configured exchange accounts."""
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        accounts = {}
        for name in manager.account_names:
            ex = manager.get_exchange(name)
            accounts[name] = {
                "exchange": ex.exchange.id,
                "sandbox": ex.exchange.sandbox,
            }
        return json.dumps(accounts, indent=2)
