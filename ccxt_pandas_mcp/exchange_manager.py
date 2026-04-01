"""Exchange lifecycle management for the MCP server."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

import ccxt.pro as ccxt_pro

from ccxt_pandas import AsyncCCXTPandasExchange
from ccxt_pandas_mcp.config import MCPServerConfig, load_config


class ExchangeManager:
    """Manages initialized AsyncCCXTPandasExchange instances."""

    def __init__(self, config: MCPServerConfig):
        self.config = config
        self._exchanges: dict[str, AsyncCCXTPandasExchange] = {}
        self._raw_exchanges: list = []

    async def initialize(self) -> None:
        """Initialize all configured exchange accounts."""
        for name, account in self.config.accounts.items():
            exchange_class = getattr(ccxt_pro, account.exchange)
            params = {
                "enableRateLimit": True,
                "defaultType": account.default_type,
                **account.extra_params,
            }
            if account.api_key:
                params["apiKey"] = account.api_key
            if account.secret.get_secret_value():
                params["secret"] = account.secret.get_secret_value()
            if account.password and account.password.get_secret_value():
                params["password"] = account.password.get_secret_value()

            raw_exchange = exchange_class(params)
            if account.sandbox_mode:
                raw_exchange.set_sandbox_mode(True)

            pandas_exchange = AsyncCCXTPandasExchange(exchange=raw_exchange)
            await pandas_exchange.load_markets()

            self._exchanges[name] = pandas_exchange
            self._raw_exchanges.append(raw_exchange)

    def get_exchange(self, account: str | None = None) -> AsyncCCXTPandasExchange:
        """Get an exchange instance by account name.

        Falls back to default_account, then the first configured account.
        Raises ValueError if no exchanges are configured.
        """
        if account and account in self._exchanges:
            return self._exchanges[account]

        if self.config.default_account and self.config.default_account in self._exchanges:
            return self._exchanges[self.config.default_account]

        if self._exchanges:
            return next(iter(self._exchanges.values()))

        raise ValueError(
            "No exchanges configured. Set CCXT_MCP_CONFIG or "
            "CCXT_MCP_ACCOUNT_<name>_EXCHANGE environment variables."
        )

    @property
    def account_names(self) -> list[str]:
        return list(self._exchanges.keys())

    async def close(self) -> None:
        """Close all exchange connections."""
        for raw in self._raw_exchanges:
            try:
                await raw.close()
            except Exception:
                pass


@asynccontextmanager
async def lifespan(server) -> AsyncIterator[dict]:
    """FastMCP lifespan — initialize and teardown exchanges."""
    config = load_config()
    manager = ExchangeManager(config)
    await manager.initialize()
    try:
        yield {"exchange_manager": manager, "config": config}
    finally:
        await manager.close()
