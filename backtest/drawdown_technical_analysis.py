import pandas as pd
import os


TRADE_FILE = "debug_export/drawdown_trades.csv"
PRICE_FILE = "debug_export/drawdown_price.csv"
TECH_FILE = "debug_export/drawdown_technical_factor.csv"

OUTPUT_DIR = "results_v4_2"


def load_data():

    trades = pd.read_csv(
        TRADE_FILE,
        parse_dates=["date"]
    )

    prices = pd.read_csv(
        PRICE_FILE,
        parse_dates=["date"]
    )

    tech = pd.read_csv(
        TECH_FILE,
        parse_dates=["date"]
    )

    return trades, prices, tech


def analyze_position(
    code,
    buy_date,
    shares,
    prices,
    tech
):

    p = prices[
        (prices.code == code)
        &
        (prices.date >= buy_date)
    ].copy()

    t = tech[
        (tech.code == code)
        &
        (tech.date >= buy_date)
    ].copy()


    if len(p) == 0:
        return None


    p = p.sort_values("date")
    t = t.sort_values("date")


    buy_price = p.iloc[0].close


    result = {

        "code": code,
        "buy_date": buy_date.date(),
        "buy_price": buy_price,
        "shares": shares,

        "buy_technical_score": None,
        "buy_trend_score": None,
        "buy_momentum_score": None,

        "break_ma20_date": None,
        "break_ma60_date": None,
        "break_ma120_date": None,

        "technical_score_low": None,

        "max_loss_after_ma60": None,

        "holding_days": len(p)

    }


    if len(t):

        first = t.iloc[0]

        result["buy_technical_score"] = first.get(
            "technical_score"
        )

        result["buy_trend_score"] = first.get(
            "trend_score"
        )

        result["buy_momentum_score"] = first.get(
            "momentum_score"
        )


        # MA跌破检测

        for ma in [
            "ma20",
            "ma60",
            "ma120"
        ]:

            name = "break_" + ma + "_date"

            tmp = t[
                t.close < t[ma]
            ]

            if len(tmp):

                result[name] = (
                    tmp.iloc[0].date.date()
                )


        if "technical_score" in t:

            result[
                "technical_score_low"
            ] = t.technical_score.min()



        # 如果 MA60 卖出

        if result["break_ma60_date"]:

            exit_date = pd.Timestamp(
                result["break_ma60_date"]
            )

            after = p[
                p.date >= exit_date
            ]

            if len(after):

                low = after.close.min()

                result[
                    "max_loss_after_ma60"
                ] = (
                    low / buy_price - 1
                )


    return result



def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    trades, prices, tech = load_data()


    # 只分析2015-2018最大回撤窗口

    trades = trades[
        (
            trades.date >= "2015-06-12"
        )
        &
        (
            trades.date <= "2018-10-18"
        )
    ]


    results=[]


    for _, row in trades.iterrows():

        if row.action != "BUY":
            continue


        r = analyze_position(
            row.code,
            row.date,
            row.shares,
            prices,
            tech
        )

        if r:
            results.append(r)



    df = pd.DataFrame(results)


    csv_file = (
        OUTPUT_DIR
        +
        "/drawdown_technical_analysis.csv"
    )


    df.to_csv(
        csv_file,
        index=False,
        encoding="utf-8-sig"
    )


    txt_file = (
        OUTPUT_DIR
        +
        "/drawdown_technical_analysis.txt"
    )


    with open(
        txt_file,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "2015-2018 最大回撤技术指标分析\n"
        )

        f.write(
            "="*60
            +
            "\n\n"
        )


        f.write(
            f"分析交易数量:{len(df)}\n\n"
        )


        for col in [
            "break_ma20_date",
            "break_ma60_date",
            "break_ma120_date"
        ]:

            count = (
                df[col]
                .notna()
                .sum()
            )

            f.write(
                f"{col}: {count}\n"
            )


        f.write("\n")


        f.write(
            "买入技术评分统计:\n"
        )

        f.write(
            str(
                df[
                    [
                    "buy_technical_score",
                    "buy_trend_score",
                    "buy_momentum_score"
                    ]
                ]
                .describe()
            )
        )

        f.write("\n\n")


        f.write(
            "跌破MA60后最大亏损统计:\n"
        )

        f.write(
            str(
                df.max_loss_after_ma60.describe()
            )
        )



    print("完成")
    print(csv_file)
    print(txt_file)



if __name__ == "__main__":
    main()