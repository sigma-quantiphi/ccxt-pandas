"""Account tools — balance, positions, orders, trades, fees, transfers."""

from __future__ import annotations

from typing import Literal

from fastmcp import Context, FastMCP

from ccxt_pandas_mcp._helpers import safe_tool, to_list
from ccxt_pandas_mcp.serialization import serialize_dataframe


def register_account_tools(mcp: FastMCP):
    # --- Balances / accounts ---

    @mcp.tool()
    @safe_tool
    async def fetch_balance(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch account balances. Requires auth.

        Returns:
            DataFrame: `currency`, `free`, `used`, `total`. Filter empty rows
            with `.query("total > 0")`.
        """
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(await ex.fetch_balance(), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_accounts(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """List sub-accounts on this exchange (where supported)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(await ex.fetch_accounts(), fmt=output_format)

    # --- Positions ---

    @mcp.tool()
    @safe_tool
    async def fetch_position(
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch position for a single symbol (returns 1-row DataFrame)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(await ex.fetch_position(symbol=symbol), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_positions(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch open derivative positions. Requires auth.

        Returns:
            DataFrame: `symbol`, `side` (`long`/`short`), `contracts`,
            `notional`, `entryPrice`, `markPrice`, `unrealizedPnl`,
            `liquidationPrice`, `leverage`, `marginMode`, `collateral`.
        """
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(await ex.fetch_positions(**kwargs), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_positions_history(
        symbols: str | list[str] | None = None,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch closed/historical positions."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_positions_history(**kwargs), fmt=output_format, max_rows=limit
        )

    # --- Orders ---

    @mcp.tool()
    @safe_tool
    async def fetch_order(
        order_id: str,
        symbol: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch a single order by ID (1-row DataFrame)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"id": order_id}
        if symbol:
            kwargs["symbol"] = symbol
        return serialize_dataframe(await ex.fetch_order(**kwargs), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_orders(
        symbol: str | None = None,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch orders (open + closed + canceled, exchange-dependent)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_orders(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_open_orders(
        symbol: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch currently open orders. Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if symbol:
            kwargs["symbol"] = symbol
        return serialize_dataframe(await ex.fetch_open_orders(**kwargs), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_closed_orders(
        symbol: str | None = None,
        since: str | None = None,
        limit: int = 50,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch closed/filled orders. Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_closed_orders(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_canceled_orders(
        symbol: str | None = None,
        since: str | None = None,
        limit: int = 50,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch canceled orders only (subset of order history)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_canceled_orders(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_canceled_and_closed_orders(
        symbol: str | None = None,
        since: str | None = None,
        limit: int = 50,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch canceled + closed orders together (no open orders)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_canceled_and_closed_orders(**kwargs), fmt=output_format, max_rows=limit
        )

    # --- Trades ---

    @mcp.tool()
    @safe_tool
    async def fetch_my_trades(
        symbol: str | None = None,
        since: str | None = None,
        limit: int = 50,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch your trade history. Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_my_trades(**kwargs), fmt=output_format, max_rows=limit
        )

    # --- Fees ---

    @mcp.tool()
    @safe_tool
    async def fetch_trading_fees(
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 200,
        ctx: Context = None,
    ) -> str:
        """Fetch maker/taker fees per symbol. Requires auth on most exchanges."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(
            await ex.fetch_trading_fees(), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_transaction_fees(
        codes: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 200,
        ctx: Context = None,
    ) -> str:
        """Fetch deposit/withdrawal fees per currency."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (cl := to_list(codes)) is not None:
            kwargs["codes"] = cl
        return serialize_dataframe(
            await ex.fetch_transaction_fees(**kwargs), fmt=output_format, max_rows=max_rows
        )

    # --- Leverage ---

    @mcp.tool()
    @safe_tool
    async def fetch_leverages(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch current leverage settings per symbol. Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_leverages(**kwargs), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_leverage_tiers(
        symbols: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 200,
        ctx: Context = None,
    ) -> str:
        """Fetch leverage tier brackets (notional → max leverage / maint margin)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (sl := to_list(symbols)) is not None:
            kwargs["symbols"] = sl
        return serialize_dataframe(
            await ex.fetch_leverage_tiers(**kwargs), fmt=output_format, max_rows=max_rows
        )

    # --- Deposits / Withdrawals / Ledger ---

    @mcp.tool()
    @safe_tool
    async def fetch_deposit_addresses(
        codes: str | list[str] | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        max_rows: int | None = 100,
        ctx: Context = None,
    ) -> str:
        """Fetch deposit addresses for currencies. Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {}
        if (cl := to_list(codes)) is not None:
            kwargs["codes"] = cl
        return serialize_dataframe(
            await ex.fetch_deposit_addresses(**kwargs), fmt=output_format, max_rows=max_rows
        )

    @mcp.tool()
    @safe_tool
    async def fetch_deposits(
        code: str | None = None,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch deposit history (optionally filtered by currency). Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if code:
            kwargs["code"] = code
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_deposits(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_withdrawals(
        code: str | None = None,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch withdrawal history. Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if code:
            kwargs["code"] = code
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_withdrawals(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_ledger(
        code: str | None = None,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch the account ledger (every credit/debit entry). Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if code:
            kwargs["code"] = code
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_ledger(**kwargs), fmt=output_format, max_rows=limit
        )

    # --- Borrowing ---

    @mcp.tool()
    @safe_tool
    async def fetch_borrow_interest(
        code: str | None = None,
        symbol: str | None = None,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch borrow interest paid (margin trading). Requires auth."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if code:
            kwargs["code"] = code
        if symbol:
            kwargs["symbol"] = symbol
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_borrow_interest(**kwargs), fmt=output_format, max_rows=limit
        )

    @mcp.tool()
    @safe_tool
    async def fetch_cross_borrow_rate(
        code: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch the current cross-margin borrow rate for one currency."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(await ex.fetch_cross_borrow_rate(code=code), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def fetch_isolated_borrow_rate(
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch the current isolated-margin borrow rate for one symbol."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        return serialize_dataframe(
            await ex.fetch_isolated_borrow_rate(symbol=symbol), fmt=output_format
        )

    # --- Transfers ---

    @mcp.tool()
    @safe_tool
    async def fetch_transfers(
        code: str | None = None,
        since: str | None = None,
        limit: int = 100,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Fetch internal wallet transfer history (e.g. spot ↔ futures)."""
        ex = ctx.lifespan_context["exchange_manager"].get_exchange(account)
        kwargs = {"limit": limit}
        if code:
            kwargs["code"] = code
        if since:
            kwargs["since"] = since
        return serialize_dataframe(
            await ex.fetch_transfers(**kwargs), fmt=output_format, max_rows=limit
        )
