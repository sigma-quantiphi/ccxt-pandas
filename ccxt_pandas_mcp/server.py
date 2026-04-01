"""ccxt-pandas MCP server entry point."""

from fastmcp import FastMCP

from ccxt_pandas_mcp.exchange_manager import lifespan
from ccxt_pandas_mcp.tools import (
    register_account_tools,
    register_calculation_tools,
    register_exchange_info_tools,
    register_market_data_tools,
    register_trading_tools,
)
from ccxt_pandas_mcp.resources import register_resources

mcp = FastMCP(
    "ccxt-pandas-mcp",
    instructions="Cryptocurrency exchange data and trading via ccxt-pandas. "
    "Fetch market data, manage orders, and run analytics — all returning DataFrames.",
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
