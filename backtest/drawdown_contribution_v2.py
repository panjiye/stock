import os
import pandas as pd
from data.query import engine


TRADE_FILE = "debug_export/drawdown_trades.csv"
PRICE_FILE = "debug_export/drawdown_price.csv"


OUTPUT_DIR = "results_v4_2"


DD_START = pd.Timestamp("2015-06-12")
DD_END = pd.Timestamp("2018-10-18")



def normalize_code(x):

    return str(x).split(".")[0].zfill(6)



def load_trades():

    df = pd.read_csv(
        TRADE_FILE
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df["code"] = (
        df["code"]
        .apply(normalize_code)
    )

    return df.sort_values(
        "date"
    )



def load_prices():

    df = pd.read_csv(
        PRICE_FILE
    )

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df["code"] = (
        df["code"]
        .apply(normalize_code)
    )

    return df



def load_industry():

    conn = engine.connect(
        DB_PATH
    )

    df = pd.read_sql(
        """
        select
            code,
            name,
            industry
        from stock_industry
        """,
        conn
    )

    conn.close()

    df["code"] = (
        df["code"]
        .apply(normalize_code)
    )

    return df



def filter_drawdown_trades(
        trades
):

    """
    保留影响最大回撤期间的交易

    买入 <= 回撤结束
    卖出 >= 回撤开始
    """

    result = []


    for code, g in trades.groupby(
        "code"
    ):


        position = 0

        holding = False


        for _, row in g.iterrows():

            if row["action"] == "BUY":

                position += row["shares"]

            else:

                position -= row["shares"]


            if (
                row["date"] <= DD_END
                and position > 0
            ):

                holding = True


        if holding:

            result.append(
                code
            )


    return trades[
        trades["code"].isin(result)
    ]



def calculate_stock_contribution(
        trades,
        prices
):


    results = []


    for code, g in trades.groupby(
        "code"
    ):


        g = g.sort_values(
            "date"
        )


        position = 0

        cost = 0

        buy_date = None


        for _, row in g.iterrows():


            if row["date"] > DD_END:

                break



            if row["action"] == "BUY":


                if position == 0:

                    buy_date = row["date"]


                position += row["shares"]

                cost += (
                    row["price"]
                    *
                    row["shares"]
                )


            else:


                position -= row["shares"]



        if position <= 0:

            continue



        avg_cost = cost / position


        price = prices[
            (prices["code"] == code)
            &
            (prices["date"] >= DD_START)
            &
            (prices["date"] <= DD_END)
        ]


        if len(price) == 0:

            continue



        price = price.sort_values(
            "date"
        )


        price["value"] = (
            price["close"]
            *
            position
        )


        peak = price["value"].max()

        bottom = price["value"].min()


        peak_date = (
            price.loc[
                price["value"].idxmax(),
                "date"
            ]
        )


        bottom_date = (
            price.loc[
                price["value"].idxmin(),
                "date"
            ]
        )


        loss = peak - bottom



        results.append(
            {
                "code": code,
                "shares": position,
                "avg_cost": avg_cost,
                "max_position_value": peak,
                "bottom_value": bottom,
                "loss_amount": loss,
                "loss_ratio": loss / peak
                    if peak != 0 else 0,
                "peak_date": peak_date,
                "bottom_date": bottom_date,
                "holding_days":
                    (
                        DD_END
                        -
                        buy_date
                    ).days
            }
        )


    return pd.DataFrame(results)



def main():


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    trades = load_trades()

    prices = load_prices()

    industry = load_industry()



    trades = filter_drawdown_trades(
        trades
    )


    df = calculate_stock_contribution(
        trades,
        prices
    )


    if len(df) == 0:

        print(
            "没有找到回撤期间持仓"
        )

        return



    df = df.merge(
        industry,
        on="code",
        how="left"
    )


    df = df.sort_values(
        "loss_amount",
        ascending=False
    )


    stock_file = os.path.join(
        OUTPUT_DIR,
        "drawdown_stock_contribution.csv"
    )


    df.to_csv(
        stock_file,
        index=False
    )



    industry_df = (
        df.groupby(
            "industry"
        )
        .agg(
            loss_amount=(
                "loss_amount",
                "sum"
            ),
            stocks=(
                "code",
                "count"
            ),
            max_position=(
                "max_position_value",
                "sum"
            )
        )
        .sort_values(
            "loss_amount",
            ascending=False
        )
        .reset_index()
    )


    industry_file = os.path.join(
        OUTPUT_DIR,
        "drawdown_industry_contribution.csv"
    )


    industry_df.to_csv(
        industry_file,
        index=False
    )



    txt_file = os.path.join(
        OUTPUT_DIR,
        "drawdown_contribution_v2.txt"
    )


    with open(
        txt_file,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "2015-2018 最大回撤贡献分析\n"
        )

        f.write(
            "="*60+"\n\n"
        )


        f.write(
            f"分析股票数量:{len(df)}\n\n"
        )


        f.write(
            "股票TOP20:\n\n"
        )


        for _, r in df.head(20).iterrows():

            f.write(
                f"{r['code']} "
                f"{r.get('name','')} "
                f"{r.get('industry','')} "
                f"亏损:"
                f"{r['loss_amount']:.2f} "
                f"回撤:"
                f"{r['loss_ratio']:.2%}\n"
            )


        f.write(
            "\n行业TOP20:\n\n"
        )


        for _, r in industry_df.head(20).iterrows():

            f.write(
                f"{r['industry']} "
                f"亏损:"
                f"{r['loss_amount']:.2f} "
                f"股票:"
                f"{r['stocks']}\n"
            )



    print("完成")
    print(stock_file)
    print(industry_file)
    print(txt_file)



if __name__ == "__main__":

    main()