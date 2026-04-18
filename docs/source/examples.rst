Examples
========

20 runnable scripts in the
`examples/ <https://github.com/sigma-quantiphi/ccxt-pandas/tree/main/examples>`_
directory cover market data, trading, analytics, WebSocket streaming, and
multi-exchange aggregation.

Market data & analysis
----------------------

- ``00_sync_basics.py`` — quickstart: OHLCV, order books, trades, funding rates
- ``01_spot_future_swap_price_volume_analysis.py`` — BTC spread and volume across contract types
- ``02_exchange_arbitrage.py`` — cross-exchange spread detection
- ``04_plot_trades.py`` — OHLCV candlestick + trade scatter (Plotly)
- ``05_plot_orderbook_depth.py`` — cumulative depth chart (Plotly)
- ``06_calculate_orderbook_vwaps.py`` — VWAP at multiple notional depths
- ``08_pricing_coin_quoted_symbols.py`` — convert coin-quoted pairs to USDT prices
- ``11_fetch_volatility_history.py`` — BTC volatility from Deribit
- ``15_open_interest_history.py`` — historical open interest with pct change

Account & trading (auth required)
---------------------------------

- ``03_fetch_private_data.py`` — trades, positions, greeks
- ``07_market_making_orders.py`` — LIMIT_MAKER and QUEUE orders
- ``09_deposits_withdrawals.py`` — deposit/withdrawal history
- ``13_delta_position.py`` — net delta across spot + derivatives
- ``18_cheapest_withdrawal_route.py`` — cheapest cross-exchange transfer rail per currency

Options
-------

- ``12_options_strategy_around_event.py`` — pick BTC call legs around an event date
- ``19_multi_exchange_greeks.py`` — aggregate option Greeks across binance/bybit/okx

WebSocket streaming
-------------------

- ``10_websockets_listen_liquidations.py`` — stream live liquidation events
- ``14_send_orders_via_websockets.py`` — place/edit orders via WebSocket

Async bulk operations
---------------------

- ``16_load_1000_ohlcv_async.py`` — bulk OHLCV with ``asyncio.gather``
- ``17_load_symbols_all_exchanges_async.py`` — load markets from every exchange

Performance
-----------

- ``20_caching_repeat_fetches.py`` — incremental ``fetch_trades`` with ``cache=True``
