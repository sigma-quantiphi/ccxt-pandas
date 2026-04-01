"""Account tools — balance, positions, orders, trades (require authentication)."""

from __future__ import annotations

from typing import Literal

from fastmcp import Context, FastMCP

from ccxt_pandas_mcp.exchange_manager import ExchangeManager
from ccxt_pandas_mcp.serialization import serialize_dataframe


def register_account_tools(mcp: FastMCP):

    @mcp.tool()
    async def fetch_balance(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch account balances.

        Returns DataFrame with columns: currency, free, used, total.
        Requires API key authentication.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.fetch_balance()
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    async def fetch_positions(
        symbols: list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch open derivative positions.

        Returns DataFrame with position details including side, contracts,
        entry price, unrealized PnL, and liquidation price.
        Requires API key authentication.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {}
        if symbols:
            kwargs["symbols"] = symbols
        df = await ex.fetch_positions(**kwargs)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    async def fetch_open_orders(
        symbol: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch currently open orders.

        Returns DataFrame with columns: id, timestamp, symbol, type, side, price, amount, status.
        Requires API key authentication.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {}
        if symbol:
            kwargs["symbol"] = symbol
        df = await ex.fetch_open_orders(**kwargs)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    async def fetch_closed_orders(
        symbol: str | None = None,
        limit: int = 50,
        since: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch closed/filled orders.

        Returns order history with fill details.
        Requires API key authentication.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {"limit": limit}
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        df = await ex.fetch_closed_orders(**kwargs)
        return serialize_dataframe(df, fmt=output_format, max_rows=limit)

    @mcp.tool()
    async def fetch_my_trades(
        symbol: str | None = None,
        limit: int = 50,
        since: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch your trade history.

        Returns DataFrame with columns: id, timestamp, symbol, side, price, amount, cost, fee.
        Requires API key authentication.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {"limit": limit}
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        df = await ex.fetch_my_trades(**kwargs)
        return serialize_dataframe(df, fmt=output_format, max_rows=limit)
