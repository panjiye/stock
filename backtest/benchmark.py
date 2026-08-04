import sqlite3
import pandas as pd
import numpy as np


DB_PATH = "database/stock.db"


EQUITY_FILE = "results/equity.csv"



# =====================================================
# 指标计算
# =====================================================

def calculate_metrics(
    df,
    value_col
):

    df = df.copy()


    df = df.sort_values(
        "date"
    )


    values = df[value_col]


    start = values.iloc[0]

    end = values.iloc[-1]


    total_return = (
        end / start - 1
    ) * 100



    days = len(df)


    annual_return = (
        (end / start)
        **
        (250 / days)
        -
        1
    ) * 100



    daily_return = (
        values
        .pct_change()
        .dropna()
    )


    volatility = (
        daily_return.std()
        *
        np.sqrt(250)
        *
        100
    )



    cumulative = (
        values /
        values.cummax()
        -
        1
    )


    max_drawdown = (
        cumulative.min()
        *
        100
    )



    sharpe = 0


    if volatility != 0:

        sharpe = (
            annual_return /
            volatility
        )



    return {

        "累计收益":
            round(total_return,2),

        "年化收益":
            round(annual_return,2),

        "最大回撤":
            round(max_drawdown,2),

        "波动率":
            round(volatility,2),

        "夏普":
            round(sharpe,2)

    }





# =====================================================
# 读取策略
# =====================================================

def load_strategy():

    df = pd.read_csv(
        EQUITY_FILE
    )


    df["date"] = pd.to_datetime(
        df["date"]
    )


    df = df[
        [
            "date",
            "total_value"
        ]
    ]


    return df





# =====================================================
# 读取指数
# =====================================================

def load_index(
    code,
    start,
    end
):


    conn = sqlite3.connect(
        DB_PATH
    )


    sql = """

    select
        date,
        close

    from index_price

    where code=?

    order by date

    """



    df = pd.read_sql(
        sql,
        conn,
        params=(
            code,
        )
    )


    conn.close()



    if df.empty:

        return None



    df["date"] = pd.to_datetime(
        df["date"]
    )



    df = df[
        (df.date>=start)
        &
        (df.date<=end)
    ]



    if df.empty:

        return None



    return df





# =====================================================
# 主程序
# =====================================================

def main():


    print("="*80)

    print(
        "Benchmark分析"
    )

    print("="*80)



    strategy = load_strategy()



    start = strategy["date"].min()

    end = strategy["date"].max()



    results=[]



    strategy_metrics = calculate_metrics(
        strategy,
        "total_value"
    )


    results.append(
        {
            "名称":
                "策略",

            **strategy_metrics

        }
    )



    benchmarks = {


        "000300.SH":
            "沪深300",


        "000905.SH":
            "中证500",


        "000852.SH":
            "中证1000",


        "399006.SZ":
            "创业板指",


        "000001.SH":
            "上证指数"

    }



    for code,name in benchmarks.items():


        df = load_index(
            code,
            start,
            end
        )


        if df is None:

            print(
                "跳过:",
                name
            )

            continue



        df = df.rename(
            columns={
                "close":
                    "value"
            }
        )



        metrics = calculate_metrics(
            df,
            "value"
        )



        results.append(
            {
                "名称":
                    name,

                **metrics

            }
        )



    result = pd.DataFrame(
        results
    )


    print()

    print("="*80)

    print(
        "Benchmark 对比"
    )

    print("="*80)



    print(
        result.to_string(
            index=False
        )
    )




if __name__ == "__main__":

    main()