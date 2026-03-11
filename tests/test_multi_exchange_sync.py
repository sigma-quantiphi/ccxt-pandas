import pandas as pd

from ccxt_pandas import CCXTPandasMultiExchange

end_date = pd.Timestamp.now(tz="UTC").floor("1d")
start_date = end_date - pd.Timedelta(hours=10)
symbols = ["BNB/USDT:USDT", "ETH/USDT:USDT"]
exchanges = (
    "binance",
    "bybit",
)
exchange = CCXTPandasMultiExchange(exchange_names=exchanges)

order_book = exchange.fetchOrderBook(symbol=symbols)
ohlcv = exchange.fetch_ohlcv(symbol=symbols, from_date=start_date, to_date=end_date)
print(ohlcv)
print(order_book)
