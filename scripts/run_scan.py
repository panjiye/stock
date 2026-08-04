import sys
import os
from datetime import datetime
import pandas as pd

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.append(BASE_DIR)


from analysis.indicator import add_indicator

from analysis.query import get_stock_list
from analysis.query import get_stock_daily

from strategy.ma_cross import check_ma_cross
from strategy.macd import check_macd

from strategy.scoring import calculate_score
from analysis.stock_score import combine_score
from analysis.fundamental import fundamental_score

stocks = get_stock_list()


print(
    "股票数量:",
    len(stocks)
)


result = []

REPORT_DIR = os.path.join(
    BASE_DIR,
    "reports"
)


os.makedirs(
    REPORT_DIR,
    exist_ok=True
)


for index,row in stocks.iterrows():

    code = row["code"]
    name = row["name"]


    try:

        df = get_stock_daily(code)


        if len(df) < 60:

            continue



        df = add_indicator(df)



        # 原始策略条件

        ma_signal = check_ma_cross(df)

        macd_signal = check_macd(df)



        if (
            ma_signal
            and macd_signal
        ):


            technical_score, detail = calculate_score(df)


            latest = df.iloc[-1]
            
            fundamental = fundamental_score(code)


            fundamental_score_value = fundamental["score"]


            total_score = combine_score(
                technical_score,
                fundamental_score_value
            )

            result.append(
                {
                    "code": code,
                    "name": name,
                    "close": round(
                        float(latest["close"]),
                        2
                    ),
                    "rsi": round(
                        float(latest["RSI"]),
                        2
                    ),
                    "technical_score": technical_score,

                    "fundamental_score": fundamental_score_value,

                    "total_score": total_score,

                    "technical_detail": detail,

                    "fundamental_detail": fundamental["detail"]
                }
            )


    except Exception as e:

        print(
            code,
            e
        )



# 评分排序

result.sort(
    key=lambda x:x["total_score"],
    reverse=True
)



print("================")

print(
    "发现:",
    len(result)
)


for item in result:

    print(item)



# =========================
# 输出CSV报告
# =========================

if result:


    report_file = os.path.join(
        REPORT_DIR,
        "scan_"
        +
        datetime.today().strftime(
            "%Y%m%d"
        )
        +
        ".csv"
    )


    report_df = pd.DataFrame(
        result
    )


    # 展开评分明细

    if "detail" in report_df.columns:


        detail_df = pd.json_normalize(
            report_df["detail"]
        )


        report_df = pd.concat(
            [
                report_df.drop(
                    columns=["detail"]
                ),
                detail_df
            ],
            axis=1
        )

    report_df["scan_date"] = datetime.today().strftime("%Y-%m-%d")
    report_df.to_csv(
        report_file,
        index=False,
        encoding="utf-8-sig"
    )


    print("================")

    print(
        "报告保存:",
        report_file
    )


else:

    print(
        "没有符合条件股票，不生成报告"
    )