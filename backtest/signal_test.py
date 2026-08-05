import sys
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)



#from analysis.query import get_stock_daily
from data.query import get_stock_daily
from analysis.indicator import add_indicator

from strategy.ma_cross import check_ma_cross
from strategy.macd import check_macd
from strategy.market_filter import check_market


def find_signals(code):

    """
    查找历史买入信号

    条件:

    MA金叉
    +
    MACD多头

    返回:
    信号列表
    """


    df = get_stock_daily(code)

    market_df = get_stock_daily(
        "000300"
    )

    market_df = add_indicator(
        market_df
    )

    if len(df) < 60:

        return []



    df = add_indicator(df)


    signals = []



    # 从第60天开始
    # 保证指标完整

    for i in range(60, len(df)):


        current = df.iloc[:i+1]


        market_current = market_df[
            market_df["date"] <= df.iloc[i]["date"]
        ]


        if len(market_current)<60:
            continue


        market_signal = check_market(
            market_current
        )


        ma_signal = check_ma_cross(
            current
        )


        macd_signal = check_macd(
            current
        )


        if (
            market_signal
            and ma_signal
            and macd_signal
        ):


            row = df.iloc[i]


            signals.append(
                {
                    "date": row["date"],
                    "close": row["close"]
                }
            )


    return signals




if __name__ == "__main__":


    code = "600519"


    result = find_signals(
        code
    )


    print(
        "股票:",
        code
    )


    print(
        "历史信号数量:",
        len(result)
    )


    for x in result:

        print(x)