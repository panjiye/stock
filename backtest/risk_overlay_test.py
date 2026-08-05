import sqlite3
import pandas as pd
import numpy as np
import os


DB_PATH = "database/stock.db"

EQUITY_FILE = "results_v4_2/equity.csv"

OUTPUT_DIR = "results_risk_overlay"


def load_index():

    conn = sqlite3.connect(DB_PATH)

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



def get_position_ratio(row):

    """
    市场风险仓位模型
    """

    close = row["close"]
    ma120 = row["ma120"]
    ma250 = row["ma250"]


    if pd.isna(ma250):
        return 1.0


    # 熊市
    if close < ma120:
        return 0.3


    # 震荡
    if close < ma250:
        return 0.6


    # 牛市
    return 1.0



def apply_overlay(equity, index):

    df = equity.copy()

    df["date"] = pd.to_datetime(df["date"])

    df = df.merge(
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


    df[
        "target_position"
    ] = df.apply(
        get_position_ratio,
        axis=1
    )


    # 原组合总资产
    df["overlay_total"] = df["total_value"]


    overlay_stock = []
    overlay_cash = []


    for _, row in df.iterrows():

        total = row["total_value"]

        target = row["target_position"]


        stock = total * target

        cash = total - stock


        overlay_stock.append(stock)
        overlay_cash.append(cash)



    df["overlay_stock"] = overlay_stock

    df["overlay_cash"] = overlay_cash


    return df



def calc_metrics(series):

    start = series.iloc[0]

    end = series.iloc[-1]


    total_return = (
        end / start - 1
    )


    years = (
        len(series)
        /
        252
    )


    annual = (
        (end/start)
        **
        (1/years)
        -
        1
    )


    peak = series.cummax()

    drawdown = (
        series / peak - 1
    )

    max_dd = drawdown.min()


    return {

        "total_return": total_return,

        "annual_return": annual,

        "max_drawdown": max_dd

    }



def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    equity = pd.read_csv(
        EQUITY_FILE
    )


    index = load_index()


    result = apply_overlay(
        equity,
        index
    )


    output = os.path.join(
        OUTPUT_DIR,
        "equity_overlay.csv"
    )


    result.to_csv(
        output,
        index=False
    )


    print(
        "输出:",
        output
    )


    print("\n原策略:")

    print(
        calc_metrics(
            equity["total_value"]
        )
    )


    print("\nRisk Overlay:")

    print(
        calc_metrics(
            result["overlay_total"]
        )
    )


    print("\n市场状态统计:")

    print(
        result["target_position"]
        .value_counts()
    )


if __name__ == "__main__":

    main()