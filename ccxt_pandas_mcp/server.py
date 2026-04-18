"""ccxt-pandas MCP server entry point."""

from fastmcp import FastMCP

from ccxt_pandas_mcp.exchange_manager import lifespan
from ccxt_pandas_mcp.resources import register_resources
from ccxt_pandas_mcp.tools import (
    register_account_tools,
    register_calculation_tools,
    register_exchange_info_tools,
    register_market_data_tools,
    register_trading_tools,
)

mcp = FastMCP(
    "ccxt-pandas-mcp",
    instructions=(
        "Cryptocurrency exchange data and trading via ccxt-pandas. "
        "Fetch market data, manage orders, and run analytics — all returning DataFrames.\n\n"
        "Safety defaults: read-only mode and sandbox-mode are ON by default. "
        "Set CCXT_MCP_READ_ONLY=false to enable trading. "
        "Trading tools (create_order, cancel_order, transfer) require explicit user approval. "
        "Row count is capped at CCXT_MCP_MAX_ROWS (default 100) per response."
    ),
    lifespan=lifespan,
)

register_exchange_info_tools(mcp)
register_market_data_tools(mcp)
register_account_tools(mcp)
register_trading_tools(mcp)
register_calculation_tools(mcp)
register_resources(mcp)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
