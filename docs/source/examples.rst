Examples
========

20 runnable examples in the
`examples/ <https://github.com/sigma-quantiphi/ccxt-pandas/tree/main/examples>`_
directory cover market data, trading, analytics, WebSocket streaming, and
multi-exchange aggregation. Most ship as paired ``.py`` + ``.ipynb`` files —
launch them in `Binder <https://mybinder.org/v2/gh/sigma-quantiphi/ccxt-pandas/HEAD?urlpath=%2Fdoc%2Ftree%2Fexamples>`_
for inline Plotly charts. The 4 async / WebSocket examples (``10``, ``14``,
``16``, ``17``) are ``.py``-only because Jupyter's running event loop breaks
``asyncio.run()`` and infinite ``while True`` loops block cells.

Market data & analysis
----------------------

- ``00_sync_basics.ipynb`` — quickstart: OHLCV, order books, trades, funding rates
- ``01_spot_future_swap_price_volume_analysis.ipynb`` — BTC spread and volume across contract types
- ``02_exchange_arbitrage.ipynb`` — cross-exchange spread detection
- ``04_plot_trades.ipynb`` — OHLCV candlestick + trade scatter (Plotly)
- ``05_plot_orderbook_depth.ipynb`` — cumulative depth chart (Plotly)
- ``06_calculate_orderbook_vwaps.ipynb`` — VWAP at multiple notional depths
- ``08_pricing_coin_quoted_symbols.ipynb`` — convert coin-quoted pairs to USDT prices
- ``11_fetch_volatility_history.ipynb`` — BTC volatility from Deribit
- ``15_open_interest_history.ipynb`` — historical open interest with pct change

Account & trading (auth required)
---------------------------------

- ``03_fetch_private_data.ipynb`` — trades, positions, greeks
- ``07_market_making_orders.ipynb`` — LIMIT_MAKER and QUEUE orders
- ``09_deposits_withdrawals.ipynb`` — deposit/withdrawal history
- ``13_delta_position.ipynb`` — net delta across spot + derivatives
- ``18_cheapest_withdrawal_route.ipynb`` — cheapest cross-exchange transfer rail per currency

Options
-------

- ``12_options_strategy_around_event.ipynb`` — pick BTC call legs around an event date
- ``19_multi_exchange_greeks.ipynb`` — aggregate option Greeks across binance/bybit/okx

WebSocket streaming (``.py``-only)
----------------------------------

- ``10_websockets_listen_liquidations.py`` — stream live liquidation events
- ``14_send_orders_via_websockets.py`` — place/edit orders via WebSocket

Async bulk operations (``.py``-only)
------------------------------------

- ``16_load_1000_ohlcv_async.py`` — bulk OHLCV with ``asyncio.gather``
- ``17_load_symbols_all_exchanges_async.py`` — load markets from every exchange

Performance
-----------

- ``20_caching_repeat_fetches.ipynb`` — incremental ``fetch_trades`` with ``cache=True``
