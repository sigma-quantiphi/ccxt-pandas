"""Calculation tools — delta exposure, PnL, trade aggregation, orderbook analytics."""

from __future__ import annotations

from typing import Literal

from fastmcp import Context, FastMCP

from ccxt_pandas import (
    calculate_delta_exposure,
    calculate_mid_price_and_spread,
    calculate_vwap_by_depth,
)
from ccxt_pandas_mcp.exchange_manager import ExchangeManager
from ccxt_pandas_mcp.serialization import serialize_dataframe


def register_calculation_tools(mcp: FastMCP):

    @mcp.tool()
    async def get_delta_exposure(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Calculate net delta exposure across all positions.

        Fetches balance, positions, and markets, then computes the net delta
        exposure per asset. Requires API key authentication.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)

        balance = await ex.fetch_balance()
        positions = await ex.fetch_positions()
        markets = await ex.load_markets()

        df = calculate_delta_exposure(balance=balance, positions=positions, markets=markets)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    async def get_orderbook_analytics(
        symbol: str,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Analyze order book depth — mid price, spread, and VWAP by depth.

        Fetches the order book and computes analytics in a single call.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)

        orderbook = await ex.fetch_order_book(symbol=symbol, limit=limit)
        mid_spread = calculate_mid_price_and_spread(orderbook)
        vwap = calculate_vwap_by_depth(orderbook)

        result = f"## {symbol} Order Book Analytics\n\n"
        result += "### Mid Price & Spread\n"
        result += serialize_dataframe(mid_spread, fmt=output_format)
        result += "\n\n### VWAP by Depth\n"
        result += serialize_dataframe(vwap, fmt=output_format)
        return result
