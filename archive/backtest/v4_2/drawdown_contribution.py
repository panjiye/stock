import os
import pandas as pd
from data.query import engine



TRADE_FILE = "debug_export/drawdown_trades.csv"
PRICE_FILE = "debug_export/drawdown_price.csv"

OUTPUT_DIR = "results_v4_2"

DRAWDOWN_END = "2018-10-18"



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

    return df



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



def calculate_trades_loss(
        trades,
        prices
):

    result = []


    for code in trades["code"].unique():


        stock_trades = (
            trades[
                trades["code"] == code
            ]
            .sort_values("date")
        )


        position = 0

        cost = 0

        buy_date = None



        for _, row in stock_trades.iterrows():


            shares = int(
                row["shares"]
            )


            if row["action"] == "BUY":


                if position == 0:

                    buy_date = row["date"]


                cost += (
                    row["price"]
                    *
                    shares
                )


                position += shares



            elif row["action"] == "SELL":


                if position <= 0:

                    continue


                avg_cost = (
                    cost / position
                )


                sell_value = (
                    row["price"]
                    *
                    shares
                )


                loss = (
                    row["price"]
                    -
                    avg_cost
                ) * shares


                result.append(
                    {
                        "code": code,
                        "buy_date": buy_date,
                        "sell_date": row["date"],
                        "shares": shares,
                        "avg_cost": avg_cost,
                        "sell_price": row["price"],
                        "loss_amount": loss,
                        "return": row["price"]/avg_cost-1,
                        "holding_days":
                            (
                                row["date"]
                                -
                                buy_date
                            ).days
                    }
                )


                position -= shares


        # 回撤结束仍持仓

        if position > 0:


            p = prices[
                prices["code"] == code
            ]


            if len(p) == 0:

                continue


            last = (
                p.sort_values("date")
                .iloc[-1]
            )


            avg_cost = (
                cost / position
            )


            loss = (
                last["close"]
                -
                avg_cost
            ) * position


            result.append(
                {
                    "code": code,
                    "buy_date": buy_date,
                    "sell_date": DRAWDOWN_END,
                    "shares": position,
                    "avg_cost": avg_cost,
                    "sell_price": last["close"],
                    "loss_amount": loss,
                    "return": last["close"]/avg_cost-1,
                    "holding_days":
                        (
                            pd.Timestamp(
                                DRAWDOWN_END
                            )
                            -
                            buy_date
                        ).days
                }
            )


    return pd.DataFrame(result)



def calculate_max_position(
        trades
):

    position = {}

    max_value = {}


    for _, row in (
        trades
        .sort_values("date")
        .iterrows()
    ):


        code = row["code"]


        if code not in position:

            position[code] = 0
            max_value[code] = 0



        if row["action"] == "BUY":

            position[code] += row["shares"]

        else:

            position[code] -= row["shares"]



        value = (
            position[code]
            *
            row["price"]
        )


        if value > max_value[code]:

            max_value[code] = value



    return max_value



def main():


    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    trades = load_trades()

    prices = load_prices()

    industry = load_industry()


    df = calculate_trades_loss(
        trades,
        prices
    )


    if len(df) == 0:

        print(
            "没有产生分析结果"
        )

        return



    max_position = calculate_max_position(
        trades
    )


    df["max_position_value"] = (
        df["code"]
        .map(max_position)
    )


    df = df.merge(
        industry,
        on="code",
        how="left"
    )


    total_loss = (
        df["loss_amount"]
        .sum()
    )


    if total_loss != 0:

        df["contribution"] = (
            df["loss_amount"]
            /
            total_loss
        )

    else:

        df["contribution"] = 0



    df = df.sort_values(
        "loss_amount"
    )


    csv_file = os.path.join(
        OUTPUT_DIR,
        "drawdown_contribution.csv"
    )


    df.to_csv(
        csv_file,
        index=False
    )



    txt_file = os.path.join(
        OUTPUT_DIR,
        "drawdown_contribution.txt"
    )


    with open(
        txt_file,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "最大回撤股票贡献分析\n"
        )

        f.write(
            "="*60
            +
            "\n\n"
        )


        f.write(
            f"股票数量: {len(df)}\n"
        )

        f.write(
            f"亏损总额: {total_loss:.2f}\n\n"
        )


        f.write(
            "亏损TOP20:\n\n"
        )


        for _, r in df.head(20).iterrows():

            f.write(
                f"{r['code']} "
                f"{r.get('name','')} "
                f"{r.get('industry','')} "
                f"亏损:{r['loss_amount']:.2f} "
                f"贡献:{r['contribution']:.2%} "
                f"持仓:{r['holding_days']}天\n"
            )



    print("完成")
    print(csv_file)
    print(txt_file)



if __name__ == "__main__":

    main()