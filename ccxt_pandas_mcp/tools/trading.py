"""Trading tools — create, edit, cancel orders (require auth + read_only=False)."""

from __future__ import annotations

from typing import Literal

import pandas as pd
from fastmcp import Context, FastMCP

from ccxt_pandas_mcp.config import MCPServerConfig
from ccxt_pandas_mcp.exchange_manager import ExchangeManager
from ccxt_pandas_mcp.serialization import serialize_dataframe


def _check_trading_allowed(config: MCPServerConfig) -> None:
    """Raise if trading is disabled."""
    if config.read_only:
        raise PermissionError(
            "Trading is disabled (read_only=True). "
            "Set CCXT_MCP_READ_ONLY=false or read_only=false in config to enable."
        )


def _check_symbol_allowed(symbol: str, config: MCPServerConfig) -> None:
    """Raise if symbol is blocked or not in allowlist."""
    if symbol in config.blocked_symbols:
        raise PermissionError(f"Symbol {symbol} is blocked in server config.")
    if config.allowed_symbols is not None and symbol not in config.allowed_symbols:
        raise PermissionError(
            f"Symbol {symbol} is not in the allowed symbols list. Allowed: {config.allowed_symbols}"
        )


def register_trading_tools(mcp: FastMCP):

    @mcp.tool()
    async def create_order(
        symbol: str,
        type: str,
        side: str,
        amount: float | None = None,
        price: float | None = None,
        cost: float | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Place a single order on the exchange.

        This will execute a REAL trade (or sandbox trade if sandbox_mode is enabled).

        Args:
            symbol: Trading pair (e.g. "BTC/USDT:USDT").
            type: Order type — "limit" or "market".
            side: "buy" or "sell".
            amount: Order quantity in base currency. Provide either amount or cost.
            price: Limit price (required for limit orders).
            cost: Order size in quote currency (alternative to amount).
            account: Account name if multiple exchanges configured.

        Requires read_only=False in server config.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)
        _check_symbol_allowed(symbol, config)

        manager: ExchangeManager = ctx_data["exchange_manager"]
        ex = manager.get_exchange(account)

        kwargs = {"symbol": symbol, "type": type, "side": side}
        if amount is not None:
            kwargs["amount"] = amount
        if price is not None:
            kwargs["price"] = price
        if cost is not None:
            kwargs["params"] = {"cost": cost}

        df = await ex.create_order(**kwargs)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    async def create_orders(
        orders_json: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Place multiple orders at once from a JSON array.

        This will execute REAL trades.

        Args:
            orders_json: JSON array of orders. Each order needs: symbol, type, side,
                and either amount or cost. Optional: price (required for limit orders).
                Example: [{"symbol":"BTC/USDT","type":"limit","side":"buy","cost":100,"price":60000}]
            account: Account name if multiple exchanges configured.

        Requires read_only=False in server config.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)

        orders = pd.read_json(orders_json, orient="records")
        for symbol in orders["symbol"].unique():
            _check_symbol_allowed(symbol, config)

        manager: ExchangeManager = ctx_data["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.create_orders(orders=orders)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    async def cancel_order(
        order_id: str,
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Cancel a single order by ID.

        Args:
            order_id: The order ID to cancel.
            symbol: Trading pair the order belongs to.
            account: Account name if multiple exchanges configured.

        Requires read_only=False in server config.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)

        manager: ExchangeManager = ctx_data["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.cancel_order(id=order_id, symbol=symbol)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    async def cancel_all_orders(
        symbol: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """Cancel all open orders, optionally filtered by symbol.

        Args:
            symbol: Cancel only orders for this symbol, or None for all.
            account: Account name if multiple exchanges configured.

        Requires read_only=False in server config.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)

        manager: ExchangeManager = ctx_data["exchange_manager"]
        ex = manager.get_exchange(account)
        kwargs = {}
        if symbol:
            kwargs["symbol"] = symbol
        df = await ex.cancel_all_orders(**kwargs)
        return serialize_dataframe(df, fmt=output_format)
