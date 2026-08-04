from analysis.query import get_stock_daily

from analysis.indicator import add_ma

from strategy.ma_cross import check_ma_cross



df = get_stock_daily(
    "600519"
)


df = add_ma(df)


result = check_ma_cross(df)


print(
    "贵州茅台 MA金叉:",
    result
)