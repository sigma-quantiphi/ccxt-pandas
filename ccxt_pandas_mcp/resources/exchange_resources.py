"""MCP resources — exchange/account discovery + implicit-method registry."""

from __future__ import annotations

import json

import ccxt
from fastmcp import Context, FastMCP

from ccxt_pandas_mcp.exchange_manager import ExchangeManager


def _registries() -> dict[str, dict]:
    """Return all <EXCHANGE>_METHOD_CONFIG dicts keyed by exchange id."""
    from ccxt_pandas.wrappers import exchange_parsers as ep

    out: dict[str, dict] = {}
    for attr in dir(ep):
        if attr.endswith("_METHOD_CONFIG") and isinstance(getattr(ep, attr), dict):
            exchange_id = attr.removesuffix("_METHOD_CONFIG").lower()
            out[exchange_id] = getattr(ep, attr)
    return out


def register_resources(mcp: FastMCP):
    @mcp.resource("exchanges://list")
    async def list_exchanges() -> str:
        """List every cryptocurrency exchange supported by CCXT (JSON array)."""
        return json.dumps(ccxt.exchanges, indent=2)

    @mcp.resource("accounts://list")
    async def list_accounts(ctx: Context) -> str:
        """List configured exchange accounts (JSON object)."""
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        accounts = {}
        for name in manager.account_names:
            ex = manager.get_exchange(name)
            accounts[name] = {
                "exchange": ex.exchange.id,
                "sandbox": getattr(ex.exchange, "sandbox", False),
            }
        return json.dumps(accounts, indent=2)

    @mcp.resource("implicit-methods://list")
    async def implicit_methods_list() -> str:
        """List exchanges that have implicit-method parser configs registered."""
        regs = _registries()
        return json.dumps(
            {ex_id: len(reg) for ex_id, reg in sorted(regs.items())},
            indent=2,
        )

    @mcp.resource("implicit-methods://{exchange}")
    async def implicit_methods_for_exchange(exchange: str) -> str:
        """List the implicit methods registered for one exchange.

        Each entry shows the method name plus its parser hints
        (`data_key`, `single_dict`, `is_write`). Pass the method name to the
        `call_exchange_method` tool with optional `params_json`.
        """
        regs = _registries()
        reg = regs.get(exchange.lower())
        if reg is None:
            return json.dumps(
                {
                    "error": f"No parser config registered for '{exchange}'",
                    "available": sorted(regs),
                },
                indent=2,
            )
        out = {}
        for name, cfg in sorted(reg.items()):
            out[name] = {
                "data_key": cfg.data_key,
                "single_dict": cfg.single_dict,
                "is_write": getattr(cfg, "is_write", False),
            }
        return json.dumps(out, indent=2)
