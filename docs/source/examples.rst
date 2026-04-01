Examples
============

Runnable example scripts are in the ``examples/`` directory:

**Market Data & Analysis**

- ``01_spot_future_swap_price_volume_analysis.py`` — BTC spread and volume across contract types
- ``02_exchange_arbitrage.py`` — Cross-exchange spread detection
- ``04_plot_trades.py`` — OHLCV candlestick and trade scatter charts (Plotly)
- ``05_plot_orderbook_depth.py`` — Cumulative depth chart (Plotly)
- ``06_calculate_orderbook_vwaps.py`` — VWAP at multiple notional depths
- ``08_pricing_coin_quoted_symbols.py`` — Convert coin-quoted pairs to USDT prices
- ``11_fetch_volatility_history.py`` — BTC volatility from Deribit
- ``15_open_interest_history.py`` — Historical open interest with pct change

**Account & Trading**

- ``03_fetch_private_data.py`` — Trades, positions, greeks (sandbox)
- ``07_market_making_orders.py`` — LIMIT_MAKER and QUEUE orders (sandbox)
- ``09_deposits_withdrawals.py`` — Deposit/withdrawal history (sandbox)
- ``13_delta_position.py`` — Net delta across spot and derivatives (sandbox)

**WebSocket Streaming**

- ``10_websockets_listen_liquidations.py`` — Stream live liquidation events
- ``14_send_orders_via_websockets.py`` — Place/edit orders via WebSocket (sandbox)

**Async Bulk Operations**

- ``16_load_1000_ohlcv_async.py`` — Fetch OHLCV for 1000 symbols in parallel
- ``17_load_symbols_all_exchanges_async.py`` — Load markets from all exchanges