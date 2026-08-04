from analysis.query import get_stock_daily

from analysis.indicator import (
    add_ma,
    add_macd,
    add_rsi,
    add_kdj
)



df = get_stock_daily(
    "600519"
)


df = add_ma(df)

df = add_macd(df)

df = add_rsi(df)

df = add_kdj(df)


print(
    df.tail(10)
)