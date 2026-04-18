"""Configuration models for ccxt-pandas MCP server."""

from __future__ import annotations

import json
import os
from pathlib import Path

from pydantic import BaseModel, Field, SecretStr


class ExchangeAccountConfig(BaseModel):
    """Configuration for a single exchange account."""

    exchange: str = Field(..., description="Exchange ID (e.g. 'binance', 'okx')")
    api_key: str = ""
    secret: SecretStr = SecretStr("")
    password: SecretStr | None = None
    sandbox_mode: bool = True
    default_type: str = "spot"
    extra_params: dict = Field(default_factory=dict)


class MCPServerConfig(BaseModel):
    """Top-level MCP server configuration."""

    accounts: dict[str, ExchangeAccountConfig] = Field(default_factory=dict)
    read_only: bool = True
    max_order_cost: float = 10_000
    allowed_symbols: list[str] | None = None
    blocked_symbols: list[str] = Field(default_factory=list)
    default_account: str | None = None
    # Withdrawal double-gate: even when read_only=False, the `withdraw` tool
    # refuses unless allow_withdrawals=True. Optionally restrict destinations.
    allow_withdrawals: bool = False
    withdraw_address_allowlist: list[str] = Field(default_factory=list)


def load_config() -> MCPServerConfig:
    """Load configuration from env vars and/or config file.

    Priority: CCXT_MCP_CONFIG file > individual env vars > defaults.
    """
    config_path = os.getenv("CCXT_MCP_CONFIG")
    if config_path and Path(config_path).exists():
        with open(config_path) as f:
            data = json.load(f)
        return MCPServerConfig(**data)

    # Build config from individual env vars
    read_only = os.getenv("CCXT_MCP_READ_ONLY", "true").lower() != "false"
    default_account = os.getenv("CCXT_MCP_DEFAULT_ACCOUNT")

    accounts: dict[str, ExchangeAccountConfig] = {}

    # Support CCXT_MCP_ACCOUNT_<name>_EXCHANGE pattern
    for key, value in os.environ.items():
        if key.startswith("CCXT_MCP_ACCOUNT_") and key.endswith("_EXCHANGE"):
            name = key.removeprefix("CCXT_MCP_ACCOUNT_").removesuffix("_EXCHANGE").lower()
            prefix = f"CCXT_MCP_ACCOUNT_{name.upper()}_"
            accounts[name] = ExchangeAccountConfig(
                exchange=value,
                api_key=os.getenv(f"{prefix}API_KEY", ""),
                secret=SecretStr(os.getenv(f"{prefix}SECRET", "")),
                password=(SecretStr(pw) if (pw := os.getenv(f"{prefix}PASSWORD")) else None),
                sandbox_mode=os.getenv(f"{prefix}SANDBOX", "true").lower() != "false",
                default_type=os.getenv(f"{prefix}TYPE", "spot"),
            )

    allow_withdrawals = os.getenv("CCXT_MCP_ALLOW_WITHDRAWALS", "false").lower() == "true"
    addr_csv = os.getenv("CCXT_MCP_WITHDRAW_ADDRESS_ALLOWLIST", "")
    address_allowlist = [a.strip() for a in addr_csv.split(",") if a.strip()]

    return MCPServerConfig(
        accounts=accounts,
        read_only=read_only,
        default_account=default_account,
        allow_withdrawals=allow_withdrawals,
        withdraw_address_allowlist=address_allowlist,
    )
