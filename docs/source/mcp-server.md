# MCP Server

ccxt-pandas includes an optional [Model Context Protocol](https://modelcontextprotocol.io/)
server that exposes exchange data and trading as tools for AI assistants like
Claude Desktop, Claude Code, and other MCP clients.

## Install

```bash
pip install "ccxt-pandas[mcp]"
```

Pulls in `fastmcp`.

## Configure

The server reads either a JSON config file or environment variables.

### Config file

```bash
export CCXT_MCP_CONFIG=/path/to/ccxt-mcp-config.json
```

```json
{
  "accounts": {
    "binance": {
      "exchange": "binance",
      "api_key": "your_api_key",
      "secret": "your_secret",
      "sandbox_mode": true
    }
  },
  "read_only": true
}
```

### Environment variables

```bash
export CCXT_MCP_ACCOUNT_BINANCE_EXCHANGE=binance
export CCXT_MCP_ACCOUNT_BINANCE_API_KEY=your_key
export CCXT_MCP_ACCOUNT_BINANCE_SECRET=your_secret
export CCXT_MCP_ACCOUNT_BINANCE_SANDBOX_MODE=true
export CCXT_MCP_READ_ONLY=true
export CCXT_MCP_MAX_ROWS=100   # default row cap on responses
```

## Run

```bash
ccxt-pandas-mcp
# or
uv run ccxt-pandas-mcp
```

## Wire into Claude Desktop / Claude Code

Add to your MCP client config:

```json
{
  "mcpServers": {
    "ccxt-pandas": {
      "command": "uv",
      "args": ["run", "ccxt-pandas-mcp"],
      "env": {
        "CCXT_MCP_CONFIG": "/path/to/ccxt-mcp-config.json"
      }
    }
  }
}
```

## Safety defaults

- **Read-only** by default. Set `CCXT_MCP_READ_ONLY=false` to enable trading
  tools (`create_order`, `cancel_order`, `transfer`, …).
- **Sandbox mode** by default. Per-account `sandbox_mode: false` to hit
  production.
- **Row cap** of 100 per response. Override with `CCXT_MCP_MAX_ROWS` or per call.
- **Trading tools require explicit user approval** in the MCP client UI.

## Available tools

20 tools across 5 categories:

- **`exchange_info`** — list configured accounts, list supported methods, fetch
  exchange capabilities.
- **`market_data`** — `fetch_ohlcv`, `fetch_order_book`, `fetch_ticker`,
  `fetch_trades`, `fetch_funding_rates`, `fetch_open_interest_history`, …
- **`account`** — `fetch_balance`, `fetch_positions`, `fetch_open_orders`,
  `fetch_closed_orders`, `fetch_my_trades`.
- **`trading`** (gated by `read_only`) — `create_order`, `cancel_order`,
  `cancel_all_orders`, `edit_order`, `transfer`.
- **`calculations`** — `calculate_vwap_by_depth`, `calculate_mid_price_and_spread`,
  `aggregate_trades`, `calculate_realized_pnl`.

## Resources

- `exchanges://list` — all CCXT-supported exchange IDs.
- `accounts://list` — currently configured accounts.

## Output format

DataFrames are serialized to markdown tables by default (also `json` and `csv`).
Truncated responses include a footer noting the row cap and how to fetch more.

## Source

See [`ccxt_pandas_mcp/`](https://github.com/sigma-quantiphi/ccxt-pandas/tree/main/ccxt_pandas_mcp)
in the repo. Built on FastMCP v3 with a lifespan-managed exchange manager.
