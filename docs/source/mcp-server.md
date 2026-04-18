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
- **Row cap** of 100 per response. Override with `CCXT_MCP_MAX_ROWS` env var,
  per-call `max_rows=<N>`, or `max_rows=0` for unlimited.
- **Trading tools require explicit user approval** in the MCP client UI.
- **Withdrawals are double-gated.** The `withdraw` tool refuses unless BOTH
  `read_only=False` AND `allow_withdrawals=True` (env: `CCXT_MCP_ALLOW_WITHDRAWALS=true`).
  Optional `withdraw_address_allowlist` further restricts destinations.
- **Errors are wrapped** by `safe_tool` — Claude sees `Error: rate limited by exchange. …`
  rather than a raw traceback.

## Available tools

72 tools across 7 categories:

- **`exchange_info`** (5) — `list_exchanges`, `list_configured_accounts`,
  `load_markets`, `fetch_currencies`, `fetch_status`.
- **`market_data`** (20) — OHLCV, order book, trades, ticker(s), bids_asks,
  mark/last prices, funding rate(s)/history/intervals, open interest (current/history/many),
  long-short ratio history, liquidations, options (volatility, chain, all greeks).
- **`account`** (24) — balance, accounts, positions (current/history/single),
  orders (open/closed/canceled/all/by-id/canceled-and-closed), my trades, fees
  (trading/transaction), leverage (current/tiers), deposit addresses, deposits,
  withdrawals, ledger, borrow interest, borrow rates (cross/isolated), transfers.
- **`trading`** (11, gated by `read_only`) — `create_order`/`create_orders`,
  `edit_order`/`edit_orders`, `cancel_order`/`cancel_all_orders`,
  `set_leverage`, `set_margin_mode`, `set_position_mode`, `transfer`,
  `withdraw` (double-gated).
- **`calculations`** (2) — `get_delta_exposure`, `get_orderbook_analytics`.
- **`implicit`** (1) — `call_exchange_method` dispatches to any of the
  ~140 exchange-specific endpoints registered in
  `ccxt_pandas/wrappers/exchange_parsers.py` (Binance Earn / algo, OKX
  Rubik / margin / lending, etc.). Discover names via the
  `implicit-methods://<exchange>` resource.
- **`okx_grid`** (8) — featured wrappers for OKX grid trading:
  `okx_grid_pending`, `okx_grid_history`, `okx_grid_details`,
  `okx_grid_sub_orders`, `okx_grid_positions`,
  `okx_grid_create`, `okx_grid_stop`, `okx_grid_modify`.

## Resources

- `exchanges://list` — all CCXT-supported exchange IDs.
- `accounts://list` — currently configured accounts.
- `implicit-methods://list` — exchanges with parser configs registered + count.
- `implicit-methods://<exchange>` — every implicit method available on one
  exchange, with `data_key`, `single_dict`, and `is_write` metadata.

## Output format

DataFrames are serialized to markdown tables by default (also `json` and `csv`).
Truncated responses include a footer noting the row cap and how to fetch more.

## Source

See [`ccxt_pandas_mcp/`](https://github.com/sigma-quantiphi/ccxt-pandas/tree/main/ccxt_pandas_mcp)
in the repo. Built on FastMCP v3 with a lifespan-managed exchange manager.
