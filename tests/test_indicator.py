from analysis.query import get_stock_daily
from analysis.indicator import add_ma



df = get_stock_daily(
    "600519"
)


df = add_ma(df)


print(
    df.tail(10)
)