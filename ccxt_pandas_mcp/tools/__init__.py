"""MCP tool registrations."""

from ccxt_pandas_mcp.tools.account import register_account_tools
from ccxt_pandas_mcp.tools.calculations import register_calculation_tools
from ccxt_pandas_mcp.tools.exchange_info import register_exchange_info_tools
from ccxt_pandas_mcp.tools.market_data import register_market_data_tools
from ccxt_pandas_mcp.tools.trading import register_trading_tools

__all__ = [
    "register_market_data_tools",
    "register_account_tools",
    "register_trading_tools",
    "register_calculation_tools",
    "register_exchange_info_tools",
]
