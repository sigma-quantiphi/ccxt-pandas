"""Market data tools — OHLCV, trades, order book, tickers, funding, OI, options."""

from __future__ import annotations

from typing import Literal

from fastmcp import Context, FastMCP

from ccxt_pandas_mcp._helpers import safe_tool, to_list
from ccxt_pandas_mcp.serialization import serialize_dataframe


def register_market_data_tools(mcp: FastMCP):
    # --- OHLCV / trades / order book / tickers ---

    @mcp.tool()
    @safe_tool
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
            symbol: e.g. `BTC/USDT`, `ETH/USDT:USDT`.
            timeframe: `1m`/`5m`/`15m`/`1h`/`4h`/`1d`/`1w`.
            limit: Per-exchange limits apply (Binance ≤1500, OKX ≤300).
            since: ISO 8601 start (`2024-01-01T00:00:00Z`).

        Returns:
            DataFrame: `timestamp` (UTC datetime64), `open`, `high`, `low`,
            `close`, `volume`. One row per candle.
        """
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"symbol": symbol, "timeframe": timeframe, "limit": limit}
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_ohlcv(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_trades(
        symbol: str,
        limit: int = 100,
        since: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch recent public trades.

        Returns:
            DataFrame: `id`, `timestamp`, `symbol`, `side`, `price`, `amount`,
            `cost`, `fees`, `exchange`.
        """
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"symbol": symbol, "limit": limit}
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_trades(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_order_book(
        symbol: str,
        limit: int = 20,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch order book depth.

        Returns:
            Long-format DataFrame: `symbol`, `side` (`bids`/`asks`), `price`,
            `qty`. Use `get_orderbook_analytics` for mid/spread/VWAP.
        """
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        df = await ex.fetch_order_book(symbol=symbol, limit=limit)
        return serialize_dataframe(df, fmt=output_format, max_rows=limit * 2)

    @mcp.tool()
    @safe_tool
    async def fetch_ticker(
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch current ticker (last/bid/ask/24h stats) for one pair."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(await ex.fetch_ticker(symbol=symbol), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_tickers(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch tickers for many (or all) pairs.

        Args:
            symbols: List or comma-separated string (`BTC/USDT,ETH/USDT`).
        """
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_tickers(**kwargs), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_bids_asks(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch best bid/ask for many pairs (cheaper than full order books)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_bids_asks(**kwargs), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_mark_prices(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch mark prices (and index prices) for derivatives."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_mark_prices(**kwargs), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_last_prices(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch last trade prices for many pairs (lighter than tickers)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_last_prices(**kwargs), fmt=output_format, max_rows=max_rows
        )

    # --- Funding ---

    @mcp.tool()
    @safe_tool
    async def fetch_funding_rate(
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch the current funding rate for one perpetual symbol."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(await ex.fetch_funding_rate(symbol=symbol), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_funding_rates(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch current funding rates for many (or all) perpetuals."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_funding_rates(**kwargs), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_funding_rate_history(
        symbol: str,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch historical funding rates for a perpetual symbol."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"symbol": symbol, "limit": limit}
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_funding_rate_history(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_funding_history(
        symbol: str | None = None,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch your funding payment history (paid/received).

        Requires API key authentication.
        """
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_funding_history(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_funding_intervals(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch funding intervals (e.g. 8h, 4h) per perpetual symbol."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_funding_intervals(**kwargs), fmt=output_format, max_rows=max_rows
        )

    # --- Open Interest / Long-Short / Liquidations ---

    @mcp.tool()
    @safe_tool
    async def fetch_open_interest(
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch current open interest for one symbol."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(await ex.fetch_open_interest(symbol=symbol), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_open_interest_history(
        symbol: str,
        timeframe: str = "1h",
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch historical open interest with `pct_change`."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"symbol": symbol, "timeframe": timeframe, "limit": limit}
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_open_interest_history(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_open_interests(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch current open interest for many (or all) symbols."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_open_interests(**kwargs), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_long_short_ratio_history(
        symbol: str,
        timeframe: str = "1h",
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch long/short account ratio time series (sentiment indicator)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"symbol": symbol, "timeframe": timeframe, "limit": limit}
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_long_short_ratio_history(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_liquidations(
        symbol: str,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch public liquidation events for a symbol."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"symbol": symbol, "limit": limit}
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_liquidations(**kwargs), fmt=output_format, max_rows=limit
        )

    # --- Options ---

    @mcp.tool()
    @safe_tool
    async def fetch_volatility_history(
        code: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 200,
        ctx: Context = None,
    ) -> str:
        """Fetch historical volatility for a base currency (e.g. `BTC` on Deribit)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(
            await ex.fetch_volatility_history(code=code), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_option_chain(
        code: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 200,
        ctx: Context = None,
    ) -> str:
        """Fetch the full option chain for a base currency."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(
            await ex.fetch_option_chain(code=code), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_all_greeks(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 200,
        ctx: Context = None,
    ) -> str:
        """Fetch Greeks (delta, gamma, vega, theta, IV) for option contracts."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_all_greeks(**kwargs), fmt=output_format, max_rows=max_rows
        )
