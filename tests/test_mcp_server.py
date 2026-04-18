"""Mocked tests for the FastMCP server — covers tool wiring, gating, and dispatcher."""

from __future__ import annotations

import json

import pytest

from ccxt_pandas_mcp._helpers import safe_tool, to_list
from ccxt_pandas_mcp.config import MCPServerConfig
from ccxt_pandas_mcp.serialization import (
    DEFAULT_MAX_ROWS,
    UNLIMITED_ROWS,
    resolve_max_rows,
)
from ccxt_pandas_mcp.tools.implicit import _is_write_method, _lookup_config
from ccxt_pandas_mcp.tools.trading import _check_symbol_allowed, _check_trading_allowed


def test_resolve_max_rows():
    assert resolve_max_rows(None) == DEFAULT_MAX_ROWS
    assert resolve_max_rows(0) == UNLIMITED_ROWS
    assert resolve_max_rows(50) == 50
    assert resolve_max_rows(1) == 1


def test_to_list_handles_csv_and_list_and_none():
    assert to_list(None) is None
    assert to_list("") is None
    assert to_list("   ") is None
    assert to_list("BTC/USDT") == ["BTC/USDT"]
    assert to_list("BTC/USDT,ETH/USDT") == ["BTC/USDT", "ETH/USDT"]
    assert to_list(" BTC/USDT , ETH/USDT ") == ["BTC/USDT", "ETH/USDT"]
    assert to_list(["BTC/USDT", "ETH/USDT"]) == ["BTC/USDT", "ETH/USDT"]
    assert to_list([]) is None


@pytest.mark.asyncio
async def test_safe_tool_wraps_ccxt_exceptions():
    import ccxt

    @safe_tool
    async def fails():
        raise ccxt.AuthenticationError("bad key")

    result = await fails()
    assert "Error: authentication failed" in result
    assert "bad key" in result


@pytest.mark.asyncio
async def test_safe_tool_wraps_permission_error():
    @safe_tool
    async def fails():
        raise PermissionError("nope")

    assert (await fails()) == "Error: nope"


@pytest.mark.asyncio
async def test_safe_tool_wraps_rate_limit():
    import ccxt

    @safe_tool
    async def fails():
        raise ccxt.RateLimitExceeded("slow down")

    assert "rate limited" in (await fails()).lower()


def test_check_trading_allowed_blocks_when_read_only():
    config = MCPServerConfig(read_only=True)
    with pytest.raises(PermissionError, match="read_only=True"):
        _check_trading_allowed(config)


def test_check_trading_allowed_passes_when_writes_enabled():
    config = MCPServerConfig(read_only=False)
    _check_trading_allowed(config)  # should not raise


def test_check_symbol_allowed_blocks_blocked_symbol():
    config = MCPServerConfig(blocked_symbols=["BTC/USDT"])
    with pytest.raises(PermissionError, match="blocked"):
        _check_symbol_allowed("BTC/USDT", config)


def test_check_symbol_allowed_enforces_allowlist():
    config = MCPServerConfig(allowed_symbols=["ETH/USDT"])
    with pytest.raises(PermissionError, match="not in the allowed"):
        _check_symbol_allowed("BTC/USDT", config)
    _check_symbol_allowed("ETH/USDT", config)  # should not raise


def test_withdraw_double_gate_defaults():
    """Withdrawals require allow_withdrawals=True even if read_only=False."""
    config = MCPServerConfig(read_only=False)
    assert config.allow_withdrawals is False
    assert config.withdraw_address_allowlist == []


def test_implicit_write_heuristic():
    # Read-style names: GET prefix, fetch_, etc.
    assert not _is_write_method("privateGetTradingBotGridOrdersAlgoPending", None)
    assert not _is_write_method("sapiGetSimpleEarnFlexibleList", None)
    assert not _is_write_method("fetch_balance", None)
    # Write-style names: POST/PUT/DELETE
    assert _is_write_method("privatePostTradingBotGridOrderAlgo", None)
    assert _is_write_method("sapiPostAlgoSpotNewOrderTwap", None)
    assert _is_write_method("privateDeleteOrder", None)


def test_implicit_write_explicit_flag_overrides():
    """is_write=True wins regardless of name pattern."""
    from ccxt_pandas.wrappers.exchange_parsers import MethodConfig

    cfg = MethodConfig(is_write=True)
    assert _is_write_method("anyReadishName", cfg)


def test_lookup_config_finds_okx_grid():
    """Phase 5 added is_write=True to OKX grid writes."""
    cfg = _lookup_config("privatePostTradingBotGridOrderAlgo", "okx")
    assert cfg is not None
    assert cfg.is_write is True
    assert cfg.data_key == "data"


@pytest.mark.asyncio
async def test_server_registers_expected_tool_count():
    from ccxt_pandas_mcp.server import mcp

    tools = await mcp._list_tools()
    names = {t.name for t in tools}
    # Spot-check landmark tools across phases
    assert "list_configured_accounts" in names  # Phase 1
    assert "fetch_status" in names  # Phase 1 / 2
    assert "fetch_deposits" in names  # Phase 2
    assert "fetch_leverages" in names  # Phase 2
    assert "set_leverage" in names  # Phase 3
    assert "withdraw" in names  # Phase 3
    assert "call_exchange_method" in names  # Phase 4
    assert "okx_grid_pending" in names  # Phase 5
    assert "okx_grid_create" in names  # Phase 5
    assert len(tools) >= 70


def test_implicit_methods_resource_exists():
    """The implicit-methods discovery resources are registered."""
    from ccxt_pandas_mcp.resources.exchange_resources import _registries

    regs = _registries()
    assert "binance" in regs
    assert "okx" in regs
    assert len(regs["okx"]) > 50
    assert len(regs["binance"]) > 50

    # OKX grid writes added in Phase 5
    assert "privatePostTradingBotGridOrderAlgo" in regs["okx"]


def test_okx_grid_create_payload_keys():
    """Sanity check that the OKX grid_create body uses OKX's expected keys."""
    body = {
        "instId": "BTC-USDT",
        "algoOrdType": "grid",
        "maxPx": "100000",
        "minPx": "50000",
        "gridNum": "20",
        "investment": "1000",
    }
    serialized = json.dumps(body)
    for required in ("instId", "algoOrdType", "maxPx", "minPx", "gridNum", "investment"):
        assert required in serialized
