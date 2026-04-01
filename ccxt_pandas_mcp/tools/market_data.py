"""Market data tools — OHLCV, trades, order book, tickers, funding rates."""

from __future__ import annotations

from typing import Literal

from fastmcp import Context, FastMCP

from ccxt_pandas_mcp.exchange_manager import ExchangeManager
from ccxt_pandas_mcp.serialization import serialize_dataframe


def register_market_data_tools(mcp: FastMCP):

    @mcp.tool()
    async def fetch_ohlcv(
        symbol: str,
        timeframe: str = "1h",
        limit: int = 100,
        since: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch OHLCV candlestick data for a trading pair.

        Args:
            symbol: Trading pair (e.g. "BTC/USDT", "ETH/USDT:USDT").
            timeframe: Candle interval (e.g. "1m", "5m", "1h", "1d").
            limit: Number of candles to fetch (max varies by exchange).
            since: Start time as ISO 8601 string (e.g. "2024-01-01T00:00:00Z").
            account: Account name if multiple exchanges configured.
            output_format: Response format — markdown, json, or csv.

        Returns DataFrame with columns: timestamp, open, high, low, close, volume.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {"symbol": symbol, "timeframe": timeframe, "limit": limit}
        if since:
            kwargs["since"] = since
        df = await ex.fetch_ohlcv(**kwargs)
        return serialize_dataframe(df, fmt=output_format, max_rows=limit)

    @mcp.tool()
    async def fetch_trades(
        symbol: str,
        limit: int = 100,
        since: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch recent public trades for a trading pair.

        Returns DataFrame with columns: id, timestamp, symbol, side, price, amount, cost.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {"symbol": symbol, "limit": limit}
        if since:
            kwargs["since"] = since
        df = await ex.fetch_trades(**kwargs)
        return serialize_dataframe(df, fmt=output_format, max_rows=limit)

    @mcp.tool()
    async def fetch_order_book(
        symbol: str,
        limit: int = 20,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch order book depth for a trading pair.

        Returns DataFrame with columns: side, price, amount (sorted by price).
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.fetch_order_book(symbol=symbol, limit=limit)
        return serialize_dataframe(df, fmt=output_format, max_rows=limit * 2)

    @mcp.tool()
    async def fetch_ticker(
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch current ticker for a trading pair.

        Returns last price, bid, ask, volume, and 24h change.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.fetch_ticker(symbol=symbol)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    async def fetch_tickers(
        symbols: list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch tickers for multiple (or all) trading pairs.

        Args:
            symbols: List of symbols, or None for all available tickers.
            account: Account name if multiple exchanges configured.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {}
        if symbols:
            kwargs["symbols"] = symbols
        df = await ex.fetch_tickers(**kwargs)
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)

    @mcp.tool()
    async def fetch_funding_rates(
        symbols: list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch current funding rates for perpetual contracts.

        Args:
            symbols: List of perpetual symbols, or None for all.
        """
        manager: ExchangeManager = ctx.lifespan_context["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {}
        if symbols:
            kwargs["symbols"] = symbols
        df = await ex.fetch_funding_rates(**kwargs)
        return serialize_dataframe(df, fmt=output_format, max_rows=max_rows)
