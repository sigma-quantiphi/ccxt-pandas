"""OKX Grid Trading — featured tools.

Wraps the `privateGetTradingBotGrid*` and `privatePostTradingBotGrid*`
endpoints so Claude doesn't have to remember them. All thin wrappers
around the implicit dispatcher; named so they show up in tool-search.

Docs: https://www.okx.com/docs-v5/en/#order-book-trading-grid-trading
"""

from __future__ import annotations

import json
from typing import Literal

import pandas as pd
from fastmcp import Context, FastMCP

from ccxt_pandas_mcp._helpers import safe_tool
from ccxt_pandas_mcp.config import MCPServerConfig
from ccxt_pandas_mcp.exchange_manager import ExchangeManager
from ccxt_pandas_mcp.serialization import serialize_dataframe


async def _okx_call(ctx, method_name: str, params: dict, account: str | None) -> pd.DataFrame:
    """Shared call path: route through ex.<method_name>(params)."""
    manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
    ex = manager.get_exchange(account)
    if not ex.exchange.id.startswith("okx"):
        raise ValueError(
            f"okx_grid_* tools require an OKX account; got {ex.exchange.id!r}. "
            "Pass account=<your_okx_account>."
        )
    method = getattr(ex, method_name, None) or getattr(ex.exchange, method_name)
    result = await method(params)
    if isinstance(result, pd.DataFrame):
        return result
    if isinstance(result, list):
        return pd.DataFrame(result)
    return pd.DataFrame([result] if result else [{}])


def register_okx_grid_tools(mcp: FastMCP):
    # --- Reads ---

    @mcp.tool()
    @safe_tool
    async def okx_grid_pending(
        algo_type: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """List currently running OKX grid bots.

        Args:
            algo_type: `grid` (spot) or `contract_grid` (perpetual).
            account: OKX account name.
        """
        params: dict = {"algoOrdType": algo_type} if algo_type else {}
        df = await _okx_call(ctx, "privateGetTradingBotGridOrdersAlgoPending", params, account)
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)

    @mcp.tool()
    @safe_tool
    async def okx_grid_history(
        algo_type: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """List historical / stopped OKX grid bots."""
        params: dict = {"algoOrdType": algo_type} if algo_type else {}
        df = await _okx_call(ctx, "privateGetTradingBotGridOrdersAlgoHistory", params, account)
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)

    @mcp.tool()
    @safe_tool
    async def okx_grid_details(
        algo_id: str,
        algo_type: str = "grid",
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch detailed config + state for one OKX grid bot."""
        params = {"algoOrdType": algo_type, "algoId": algo_id}
        df = await _okx_call(ctx, "privateGetTradingBotGridOrdersAlgoDetails", params, account)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def okx_grid_sub_orders(
        algo_id: str,
        sub_type: str = "live",
        algo_type: str = "grid",
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """List the sub-orders inside one OKX grid bot.

        Args:
            algo_id: Grid algo ID.
            sub_type: `live` or `filled`.
            algo_type: `grid` or `contract_grid`.
        """
        params = {"algoOrdType": algo_type, "algoId": algo_id, "type": sub_type}
        df = await _okx_call(ctx, "privateGetTradingBotGridSubOrders", params, account)
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)

    @mcp.tool()
    @safe_tool
    async def okx_grid_positions(
        algo_id: str,
        algo_type: str = "contract_grid",
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch positions held by one OKX contract-grid bot."""
        params = {"algoOrdType": algo_type, "algoId": algo_id}
        df = await _okx_call(ctx, "privateGetTradingBotGridPositions", params, account)
        return serialize_dataframe(df, fmt=output_format)

    # --- Writes (gated) ---

    def _check_writes(ctx) -> None:
        config: MCPServerConfig = ctx.lifespan_context["config"]
        if config.read_only:
            raise PermissionError(
                "OKX grid writes require read_only=False. Set CCXT_MCP_READ_ONLY=false."
            )

    @mcp.tool()
    @safe_tool
    async def okx_grid_create(
        symbol: str,
        algo_type: str,
        max_price: float,
        min_price: float,
        grid_num: int,
        investment: float,
        direction: str | None = None,
        leverage: float | None = None,
        params_json: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL CREATE A REAL OKX GRID BOT** (spot or contract).

        Args:
            symbol: OKX instrument ID (e.g. `BTC-USDT` or `BTC-USDT-SWAP`).
            algo_type: `grid` (spot) or `contract_grid` (perpetual).
            max_price: Upper price bound of the grid.
            min_price: Lower price bound of the grid.
            grid_num: Number of grid levels.
            investment: Total investment in quote currency.
            direction: For contract grid: `long`, `short`, or `neutral`.
            leverage: For contract grid: leverage to use.
            params_json: Extra OKX-specific parameters as JSON.
        """
        _check_writes(ctx)
        body = {
            "instId": symbol,
            "algoOrdType": algo_type,
            "maxPx": str(max_price),
            "minPx": str(min_price),
            "gridNum": str(grid_num),
            "investment": str(investment),
        }
        if direction:
            body["direction"] = direction
        if leverage:
            body["lever"] = str(leverage)
        if params_json:
            body.update(json.loads(params_json))
        df = await _okx_call(ctx, "privatePostTradingBotGridOrderAlgo", body, account)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def okx_grid_stop(
        algo_id: str,
        symbol: str,
        algo_type: str = "grid",
        stop_type: str = "1",
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL STOP A REAL OKX GRID BOT**.

        Args:
            algo_id: Grid algo ID.
            symbol: OKX instrument ID (e.g. `BTC-USDT`).
            algo_type: `grid` or `contract_grid`.
            stop_type: `1` = sell base + cancel orders; `2` = keep position
                (contract-grid only).
        """
        _check_writes(ctx)
        body = [
            {
                "algoId": algo_id,
                "instId": symbol,
                "algoOrdType": algo_type,
                "stopType": stop_type,
            }
        ]
        df = await _okx_call(ctx, "privatePostTradingBotGridStopOrderAlgo", body, account)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def okx_grid_modify(
        algo_id: str,
        sl_trigger_price: float | None = None,
        tp_trigger_price: float | None = None,
        algo_type: str = "grid",
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL MODIFY A LIVE OKX GRID BOT**'s stop-loss / take-profit triggers.

        Args:
            algo_id: Grid algo ID.
            sl_trigger_price: New stop-loss trigger price.
            tp_trigger_price: New take-profit trigger price.
        """
        _check_writes(ctx)
        body = {"algoId": algo_id, "algoOrdType": algo_type}
        if sl_trigger_price is not None:
            body["slTriggerPx"] = str(sl_trigger_price)
        if tp_trigger_price is not None:
            body["tpTriggerPx"] = str(tp_trigger_price)
        df = await _okx_call(ctx, "privatePostTradingBotGridAmendOrderAlgo", body, account)
        return serialize_dataframe(df, fmt=output_format)
