from data.query import (
    get_stock_daily,
    get_stock_list,
    get_latest_price
)



print("测试单股票")


df = get_stock_daily(
    "600519"
)


print(df.head())

print(
    "数据量:",
    len(df)
)



print("\n测试股票列表")


stocks = get_stock_list()

print(
    stocks.head()
)


print(
    "股票数量:",
    len(stocks)
)



print("\n测试最新行情")


latest = get_latest_price()

print(
    latest.head()
)

print(
    "最新数量:",
    len(latest)
)