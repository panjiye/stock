import os
import pandas as pd
import numpy as np
from data.query import engine


RESULT_DIR = "results_v4_2"


def load_equity():

    path = os.path.join(
        RESULT_DIR,
        "equity.csv"
    )

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = df.sort_values(
        "date"
    )

    return df



def calculate_drawdown(
    equity
):

    equity["high_water"] = (
        equity["total_value"]
        .cummax()
    )

    equity["drawdown"] = (
        equity["total_value"]
        /
        equity["high_water"]
        -
        1
    )

    return equity



def find_max_drawdown(
    equity
):

    idx = equity["drawdown"].idxmin()

    end_date = (
        equity.loc[idx,"date"]
    )

    start_idx = (
        equity.loc[:idx,"total_value"]
        .idxmax()
    )

    start_date = (
        equity.loc[start_idx,"date"]
    )


    return {

        "start":
            start_date,

        "end":
            end_date,

        "drawdown":
            equity.loc[idx,"drawdown"]

    }



def load_market():

    conn = engine.connect(
        DB_PATH
    )

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

    df["date"] = pd.to_datetime(
        df["date"]
    )

    return df



def market_return(
    start,
    end
):

    market = load_market()

    data = market[
        (market.date >= start)
        &
        (market.date <= end)
    ]

    if len(data)<2:

        return None


    return (
        data.close.iloc[-1]
        /
        data.close.iloc[0]
        -
        1
    )



def save_report(
    result
):

    out = os.path.join(
        RESULT_DIR,
        "drawdown_analysis.txt"
    )


    with open(
        out,
        "w",
        encoding="utf-8"
    ) as f:

        for k,v in result.items():

            f.write(
                f"{k}: {v}\n"
            )


    return out



def main():

    print("="*60)
    print("回撤分析报告")
    print("="*60)


    equity = load_equity()

    equity = calculate_drawdown(
        equity
    )


    dd = find_max_drawdown(
        equity
    )


    print()

    print("最大回撤周期")

    print(
        "开始:",
        dd["start"]
    )

    print(
        "结束:",
        dd["end"]
    )

    print(
        "最大回撤:",
        f"{dd['drawdown']:.2%}"
    )


    mret = market_return(
        dd["start"],
        dd["end"]
    )


    print()

    print("同期沪深300表现")

    print(
        f"{mret:.2%}"
    )


    result={

        "最大回撤开始":
            dd["start"],

        "最大回撤结束":
            dd["end"],

        "策略最大回撤":
            f"{dd['drawdown']:.2%}",

        "沪深300同期收益":
            f"{mret:.2%}"

    }


    file = save_report(
        result
    )


    print()

    print(
        "报告保存:",
        file
    )


if __name__=="__main__":

    main()