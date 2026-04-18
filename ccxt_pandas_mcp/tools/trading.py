"""Trading tools — create, edit, cancel orders (require auth + read_only=False)."""

from __future__ import annotations

from typing import Literal

import pandas as pd
from fastmcp import Context, FastMCP

from ccxt_pandas_mcp._helpers import safe_tool
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
    @safe_tool
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
        """**THIS WILL PLACE A REAL ORDER** (or sandbox if `sandbox_mode=True`).

        Place a single order on the exchange.

        Args:
            symbol: Trading pair (e.g. `BTC/USDT:USDT`).
            type: `limit` or `market`.
            side: `buy` or `sell`.
            amount: Quantity in base currency. Provide either `amount` or `cost`.
            price: Limit price (required for limit orders).
            cost: Order size in quote currency (alternative to `amount`).
            account: Account name; defaults to first configured.

        Requires `read_only=False` in server config.
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
    @safe_tool
    async def create_orders(
        orders_json: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL PLACE REAL ORDERS** (or sandbox if `sandbox_mode=True`).

        Place multiple orders at once from a JSON array.

        Args:
            orders_json: JSON array of orders. Each needs `symbol`, `type`,
                `side`, and either `amount` or `cost`. Optional: `price`
                (required for limit orders).
                Example: `[{"symbol":"BTC/USDT","type":"limit","side":"buy","cost":100,"price":60000}]`
            account: Account name; defaults to first configured.

        Requires `read_only=False` in server config.
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
    @safe_tool
    async def cancel_order(
        order_id: str,
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL CANCEL A REAL ORDER**.

        Cancel a single order by ID.

        Args:
            order_id: The order ID to cancel.
            symbol: Trading pair the order belongs to.
            account: Account name; defaults to first configured.

        Requires `read_only=False` in server config.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)

        manager: ExchangeManager = ctx_data["exchange_manager"]
        ex = manager.get_exchange(account)
        df = await ex.cancel_order(id=order_id, symbol=symbol)
        return serialize_dataframe(df, fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def cancel_all_orders(
        symbol: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL CANCEL REAL ORDERS**.

        Cancel all open orders, optionally filtered by symbol.

        Args:
            symbol: Cancel only orders for this symbol, or None for all.
            account: Account name; defaults to first configured.

        Requires `read_only=False` in server config.
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

    # --- Edit ---

    @mcp.tool()
    @safe_tool
    async def edit_order(
        order_id: str,
        symbol: str,
        type: str,
        side: str,
        amount: float | None = None,
        price: float | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL EDIT A REAL ORDER** (or sandbox if `sandbox_mode=True`).

        Cancel-and-replace a single order with new parameters.

        Args:
            order_id: ID of the order to replace.
            symbol: Trading pair.
            type: New order type (`limit` / `market`).
            side: `buy` or `sell`.
            amount: New quantity in base currency.
            price: New limit price.

        Requires `read_only=False`.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)
        _check_symbol_allowed(symbol, config)

        ex = ctx_data["exchange_manager"].get_exchange(account)
        kwargs = {"id": order_id, "symbol": symbol, "type": type, "side": side}
        if amount is not None:
            kwargs["amount"] = amount
        if price is not None:
            kwargs["price"] = price
        return serialize_dataframe(await ex.edit_order(**kwargs), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def edit_orders(
        orders_json: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL EDIT REAL ORDERS** (or sandbox if `sandbox_mode=True`).

        Cancel-and-replace multiple orders from a JSON array. Each entry needs
        `id`, `symbol`, `side`, `type`, `amount` (and `price` for limits).
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)

        orders = pd.read_json(orders_json, orient="records")
        for symbol in orders["symbol"].unique():
            _check_symbol_allowed(symbol, config)

        ex = ctx_data["exchange_manager"].get_exchange(account)
        return serialize_dataframe(await ex.edit_orders(orders=orders), fmt=output_format)

    # --- Position config ---

    @mcp.tool()
    @safe_tool
    async def set_leverage(
        leverage: int,
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS CHANGES LIVE POSITION RISK**. Set leverage for a symbol."""
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)
        _check_symbol_allowed(symbol, config)

        ex = ctx_data["exchange_manager"].get_exchange(account)
        result = await ex.exchange.set_leverage(leverage, symbol)
        import pandas as _pd

        return serialize_dataframe(_pd.DataFrame([result] if result else [{}]), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def set_margin_mode(
        margin_mode: str,
        symbol: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS CHANGES LIVE POSITION RISK**. Set `cross` or `isolated` margin."""
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)
        _check_symbol_allowed(symbol, config)

        ex = ctx_data["exchange_manager"].get_exchange(account)
        result = await ex.exchange.set_margin_mode(margin_mode, symbol)
        import pandas as _pd

        return serialize_dataframe(_pd.DataFrame([result] if result else [{}]), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def set_position_mode(
        hedged: bool,
        symbol: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS CHANGES LIVE POSITION RISK**. Toggle hedge / one-way mode.

        Args:
            hedged: True for hedged (long+short same symbol), False for one-way.
            symbol: Optional symbol scope.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)
        if symbol:
            _check_symbol_allowed(symbol, config)

        ex = ctx_data["exchange_manager"].get_exchange(account)
        kwargs = {}
        if symbol:
            kwargs["symbol"] = symbol
        result = await ex.exchange.set_position_mode(hedged, **kwargs)
        import pandas as _pd

        return serialize_dataframe(_pd.DataFrame([result] if result else [{}]), fmt=output_format)

    # --- Transfers + Withdrawals ---

    @mcp.tool()
    @safe_tool
    async def transfer(
        code: str,
        amount: float,
        from_account: str,
        to_account: str,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS MOVES REAL FUNDS BETWEEN INTERNAL WALLETS** (e.g. spot ↔ futures).

        Args:
            code: Currency code (e.g. `USDT`).
            amount: Amount to move.
            from_account: Source wallet (`spot`, `futures`, `swap`, `margin`, …).
            to_account: Destination wallet.

        Requires `read_only=False`.
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)

        ex = ctx_data["exchange_manager"].get_exchange(account)
        result = await ex.exchange.transfer(code, amount, from_account, to_account)
        import pandas as _pd

        return serialize_dataframe(_pd.DataFrame([result]), fmt=output_format)

    @mcp.tool()
    @safe_tool
    async def withdraw(
        code: str,
        amount: float,
        address: str,
        tag: str | None = None,
        network: str | None = None,
        account: str | None = None,
        output_format: Literal["markdown", "json", "csv"] = "markdown",
        ctx: Context = None,
    ) -> str:
        """**THIS WILL WITHDRAW REAL FUNDS FROM THE EXCHANGE**.

        Double-gated: requires `read_only=False` AND `allow_withdrawals=True`.
        Optionally enforced against `withdraw_address_allowlist`.

        Args:
            code: Currency code (e.g. `BTC`).
            amount: Amount to withdraw.
            address: Destination address.
            tag: Memo / destination tag (XRP, XLM, ATOM, …).
            network: Specific network (`ERC20`, `BEP20`, `TRC20`, …).
        """
        ctx_data = ctx.lifespan_context
        config: MCPServerConfig = ctx_data["config"]
        _check_trading_allowed(config)
        if not config.allow_withdrawals:
            raise PermissionError(
                "Withdrawals are disabled. Set CCXT_MCP_ALLOW_WITHDRAWALS=true "
                "(or allow_withdrawals=true in config) to enable. Both "
                "read_only=False AND allow_withdrawals=True are required."
            )
        if config.withdraw_address_allowlist and address not in config.withdraw_address_allowlist:
            raise PermissionError(
                f"Address {address} is not in withdraw_address_allowlist. "
                f"Allowed: {config.withdraw_address_allowlist}"
            )

        ex = ctx_data["exchange_manager"].get_exchange(account)
        params = {}
        if network:
            params["network"] = network
        result = await ex.exchange.withdraw(code, amount, address, tag, params)
        import pandas as _pd

        return serialize_dataframe(_pd.DataFrame([result]), fmt=output_format)
