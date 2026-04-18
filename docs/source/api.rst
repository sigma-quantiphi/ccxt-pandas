API Reference
=============

Exchange wrappers
-----------------

.. autoclass:: ccxt_pandas.CCXTPandasExchange
   :members:
   :show-inheritance:

.. autoclass:: ccxt_pandas.AsyncCCXTPandasExchange
   :members:
   :show-inheritance:

.. autoclass:: ccxt_pandas.CCXTPandasMultiExchange
   :members:
   :show-inheritance:

.. autoclass:: ccxt_pandas.AsyncCCXTPandasMultiExchange
   :members:
   :show-inheritance:

.. autoclass:: ccxt_pandas.CCXTPandasMultiAccount
   :members:
   :show-inheritance:

.. autoclass:: ccxt_pandas.AsyncCCXTPandasMultiAccount
   :members:
   :show-inheritance:

Exceptions
----------

.. autoexception:: ccxt_pandas.CCXTPandasError
.. autoexception:: ccxt_pandas.CCXTPandasOrderError
.. autoexception:: ccxt_pandas.CCXTPandasSchemaError
.. autoexception:: ccxt_pandas.CCXTPandasMethodError

Calculation utilities
---------------------

.. autofunction:: ccxt_pandas.calculate_delta_exposure
.. autofunction:: ccxt_pandas.calculate_mid_price_and_spread
.. autofunction:: ccxt_pandas.calculate_notional
.. autofunction:: ccxt_pandas.calculate_vwap_by_depth
.. autofunction:: ccxt_pandas.aggregate_trades
.. autofunction:: ccxt_pandas.calculate_realized_pnl
.. autofunction:: ccxt_pandas.floor_series
.. autofunction:: ccxt_pandas.ceil_series
.. autofunction:: ccxt_pandas.create_mirrored_sides
.. autofunction:: ccxt_pandas.is_ask_side
.. autofunction:: ccxt_pandas.side_sign
.. autofunction:: ccxt_pandas.signed_price
.. autofunction:: ccxt_pandas.sort_orderbook

Pandera schemas
---------------

.. autoclass:: ccxt_pandas.OHLCVSchema
.. autoclass:: ccxt_pandas.OrderBookSchema
.. autoclass:: ccxt_pandas.TradeSchema
.. autoclass:: ccxt_pandas.MyTradesSchema
.. autoclass:: ccxt_pandas.OrderSchema
.. autoclass:: ccxt_pandas.OrdersSchema
.. autoclass:: ccxt_pandas.BalanceSchema
.. autoclass:: ccxt_pandas.PositionsSchema
.. autoclass:: ccxt_pandas.PositionsHistorySchema
.. autoclass:: ccxt_pandas.PositionsADLRankSchema
.. autoclass:: ccxt_pandas.MarketSchema
.. autoclass:: ccxt_pandas.CurrencySchema
.. autoclass:: ccxt_pandas.TickersSchema
.. autoclass:: ccxt_pandas.BidsAsksSchema
.. autoclass:: ccxt_pandas.MarkPricesSchema
.. autoclass:: ccxt_pandas.LastPricesSchema
.. autoclass:: ccxt_pandas.FundingRateSchema
.. autoclass:: ccxt_pandas.FundingRateHistorySchema
.. autoclass:: ccxt_pandas.FundingHistorySchema
.. autoclass:: ccxt_pandas.FundingIntervalsSchema
.. autoclass:: ccxt_pandas.OpenInterestHistorySchema
.. autoclass:: ccxt_pandas.LongShortRatioSchema
.. autoclass:: ccxt_pandas.LiquidationsSchema
.. autoclass:: ccxt_pandas.GreeksSchema
.. autoclass:: ccxt_pandas.VolatilityHistorySchema
.. autoclass:: ccxt_pandas.LedgerSchema
.. autoclass:: ccxt_pandas.TransactionsSchema
.. autoclass:: ccxt_pandas.TransfersSchema
.. autoclass:: ccxt_pandas.AddressesSchema
.. autoclass:: ccxt_pandas.AccountsSchema
.. autoclass:: ccxt_pandas.PortfoliosSchema
.. autoclass:: ccxt_pandas.PortfolioDetailsSchema
.. autoclass:: ccxt_pandas.MarginsBalanceSchema
.. autoclass:: ccxt_pandas.LeveragesSchema
.. autoclass:: ccxt_pandas.BorrowInterestSchema
.. autoclass:: ccxt_pandas.CrossBorrowRatesSchema
.. autoclass:: ccxt_pandas.IsolatedBorrowRatesSchema
.. autoclass:: ccxt_pandas.TradingFeesSchema
.. autoclass:: ccxt_pandas.DepositWithdrawFeesSchema
