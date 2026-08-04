from analysis.query import get_stock_daily
from analysis.indicator import add_ma
from strategy.ma_cross import find_ma_cross


df = get_stock_daily(
    "600519"
)


df = add_ma(df)


signals = find_ma_cross(df)


print(
    "金叉次数:",
    len(signals)
)


print(
    signals[-10:]
)