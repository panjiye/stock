import os
import pandas as pd
import numpy as np
from data.query import engine



EQUITY_FILE = "results_v4_2/equity.csv"

OUTPUT_DIR = "results_risk_overlay"


def load_equity():

    df = pd.read_csv(EQUITY_FILE)

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    df["stock_return"] = (
        df["stock_value"]
        /
        df["stock_value"].shift(1)
        - 1
    )

    df["stock_return"] = (
        df["stock_return"]
        .fillna(0)
    )

    return df



def load_index():

    conn = engine.connect(DB_PATH)

    df = pd.read_sql(
        """
        select
            date,
            close
        from index_price
        where code='000300.SH'
        order by date
        """,
        conn
    )

    conn.close()

    df["date"] = pd.to_datetime(df["date"])

    df["ma120"] = (
        df["close"]
        .rolling(120)
        .mean()
    )

    df["ma250"] = (
        df["close"]
        .rolling(250)
        .mean()
    )

    return df



def market_position(row):

    """
    市场仓位模型
    """

    if pd.isna(row["ma250"]):

        return 1.0


    close = row["close"]

    ma120 = row["ma120"]

    ma250 = row["ma250"]


    if close < ma120:

        return 0.3


    elif close < ma250:

        return 0.6


    else:

        return 1.0



def simulate(equity, index):

    df = equity.merge(
        index[
            [
                "date",
                "close",
                "ma120",
                "ma250"
            ]
        ],
        on="date",
        how="left"
    )


    df["target_position"] = (
        df.apply(
            market_position,
            axis=1
        )
    )


    initial_capital = (
        df.iloc[0]["total_value"]
    )


    cash = (
        initial_capital
        *
        (1-df.iloc[0]["target_position"])
    )


    stock = (
        initial_capital
        *
        df.iloc[0]["target_position"]
    )


    result = []


    previous_position = (
        df.iloc[0]["target_position"]
    )


    for i,row in df.iterrows():


        if i != df.index[0]:

            # 股票组合跟随原策略涨跌

            stock *= (
                1
                +
                row["stock_return"]
            )


        total = cash + stock


        target = row["target_position"]


        # 调仓

        target_stock = total * target


        cash = total - target_stock

        stock = target_stock


        result.append(
            {
                "date": row["date"],
                "cash": cash,
                "stock": stock,
                "total_value": total,
                "position": target
            }
        )


    return pd.DataFrame(result)



def calc_metrics(series):

    start = series.iloc[0]

    end = series.iloc[-1]


    total_return = (
        end/start-1
    )


    years = (
        len(series)
        /
        252
    )


    annual_return = (
        (end/start)
        **
        (1/years)
        -
        1
    )


    peak = series.cummax()

    drawdown = (
        series/peak-1
    )


    max_drawdown = (
        drawdown.min()
    )


    return {

        "total_return": float(total_return),

        "annual_return": float(annual_return),

        "max_drawdown": float(max_drawdown)

    }



def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    equity = load_equity()

    index = load_index()


    overlay = simulate(
        equity,
        index
    )


    file = os.path.join(
        OUTPUT_DIR,
        "overlay_equity.csv"
    )


    overlay.to_csv(
        file,
        index=False
    )


    print(
        "输出:",
        file
    )


    print("\n原策略")

    print(
        calc_metrics(
            equity["total_value"]
        )
    )


    print("\nRisk Overlay")

    print(
        calc_metrics(
            overlay["total_value"]
        )
    )


    print("\n仓位统计")

    print(
        overlay["position"]
        .value_counts()
    )



if __name__ == "__main__":

    main()