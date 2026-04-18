"""Generic implicit-method dispatcher.

Exposes the ~140 exchange-specific endpoints registered in
`ccxt_pandas.wrappers.exchange_parsers` (Binance Earn / algo, OKX grid /
margin / Rubik, etc.) through a single MCP tool. Discovery happens via
the `implicit-methods://<exchange>` resource.
"""

from __future__ import annotations

import json
import re
from typing import Literal

import pandas as pd
from fastmcp import Context, FastMCP

from ccxt_pandas_mcp._helpers import safe_tool
from ccxt_pandas_mcp.config import MCPServerConfig
from ccxt_pandas_mcp.exchange_manager import ExchangeManager
from ccxt_pandas_mcp.serialization import serialize_dataframe

# Heuristic for write detection by method name. The MethodConfig.is_write
# flag takes precedence; this is the fallback for methods without an explicit
# annotation and for methods not registered in any parser config at all.
# Matches camelCase like `privatePostTradingBotGridOrderAlgo` (Post followed
# by uppercase or end-of-string) AND snake_case like `private_post_…`.
_WRITE_PATTERN = re.compile(
    r"(?:Post|Put|Patch|Delete)(?:[A-Z]|$)|(?:^|_)(?:post|put|patch|delete)(?:_|$)"
)


def _is_write_method(method_name: str, config_entry) -> bool:
    """Check whether an implicit method name should be treated as a write.

    Priority: explicit `is_write=True` in MethodConfig > regex heuristic.
    """
    if config_entry is not None and getattr(config_entry, "is_write", False):
        return True
    return bool(_WRITE_PATTERN.search(method_name))


def _lookup_config(method_name: str, exchange_id: str):
    """Look up the MethodConfig for a given method, if any."""
    from ccxt_pandas.wrappers import exchange_parsers as ep

    registry_name = f"{exchange_id.upper()}_METHOD_CONFIG"
    registry = getattr(ep, registry_name, None)
    if registry is None:
        return None
    return registry.get(method_name)


def register_implicit_tools(mcp: FastMCP):
    @mcp.tool()
    @safe_tool
    async def call_exchange_method(
        method_name: str,
        params_json: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = None,
        ctx: Context = None,
    ) -> str:
        """Call any implicit / exchange-specific CCXT method.

        Use this to access endpoints not exposed as dedicated MCP tools —
        Binance Earn, Binance algo orders, OKX grid trading, OKX Rubik
        statistics, margin lending, etc. Discover available methods via the
        `implicit-methods://<exchange>` resource.

        Args:
            method_name: camelCase or snake_case method name
                (e.g. `privateGetTradingBotGridOrdersAlgoPending`).
            params_json: JSON object of parameters
                (e.g. `{"instId": "BTC-USDT", "limit": 50}`).
            account: Account name; defaults to first configured.

        Write methods (POST/PUT/DELETE-style names, or any with
        `is_write=True` in their MethodConfig) require `read_only=False`.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        manager: ExchangeManager = ctx_data["exchange_manager"]
        ex = manager.get_exchange(account)

        cfg_entry = _lookup_config(method_name, ex.exchange.id)
        if _is_write_method(method_name, cfg_entry) and config.read_only:
            raise PermissionError(
                f"Method '{method_name}' looks like a write operation and "
                "read_only=True. Set CCXT_MCP_READ_ONLY=false to enable, "
                "or pass a read-only method name."
            )

        method = getattr(ex, method_name, None) or getattr(ex.exchange, method_name, None)
        if method is None:
            raise ValueError(
                f"Exchange '{ex.exchange.id}' has no method named '{method_name}'. "
                f"Check the implicit-methods://{ex.exchange.id} resource for valid names."
            )

        params = json.loads(params_json) if params_json else {}
        result = await method(params) if params else await method()

        if isinstance(result, pd.DataFrame):
            return serialize_dataframe(result, fmt=output_format, max_rows=max_rows)
        if isinstance(result, list):
            df = pd.DataFrame(result)
        elif isinstance(result, dict):
            df = pd.DataFrame([result])
        else:
            return str(result)
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)
