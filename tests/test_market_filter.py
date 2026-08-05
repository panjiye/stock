from data.query import get_index_daily
from analysis.indicator import add_indicator
from strategy.market_filter import check_market


df = get_index_daily(
    "000300"
)


df = add_indicator(df)


result = check_market(df)


print(
    "沪深300交易环境:",
    result
)


print(
    df.iloc[-1][
        [
            "date",
            "close",
            "MA60"
        ]
    ]
)