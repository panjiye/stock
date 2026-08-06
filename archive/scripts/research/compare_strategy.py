import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ============================================================
# 文件
# ============================================================

STRATEGY_FILE = "backtest_equity_cost.csv"

BENCHMARK_FILE = "benchmark.csv"


# ============================================================
# 读取策略
# ============================================================


def load_strategy():

    print("=" * 60)
    print("读取策略净值")


    df = pd.read_csv(
        STRATEGY_FILE
    )


    df["date"] = pd.to_datetime(
        df["sell_date"]
    )


    df["strategy"] = (
        df["value"]
        /
        df.iloc[0]["value"]
    )


    result = df[
        [
            "date",
            "strategy"
        ]
    ]


    print(
        "策略记录:",
        len(result)
    )


    return result



# ============================================================
# 读取Benchmark
# ============================================================


def load_benchmark():


    print("=" * 60)
    print("读取沪深300")


    df=pd.read_csv(
        BENCHMARK_FILE
    )


    df["date"]=pd.to_datetime(
        df["date"]
    )


    return df[
        [
            "date",
            "benchmark"
        ]
    ]



# ============================================================
# 转季度
# ============================================================


def convert_quarter(df):


    df=df.copy()


    df["quarter"]=(
        df["date"]
        .dt.to_period("Q")
    )


    df=(

        df
        .groupby(
            "quarter"
        )
        .last()
        .reset_index()

    )


    return df[
        [
            "date",
            "benchmark"
        ]
    ]



# ============================================================
# 合并
# ============================================================


def compare():

    strategy=load_strategy()


    benchmark=load_benchmark()


    benchmark=convert_quarter(
        benchmark
    )


    print("=" * 60)
    print("合并")


    df=strategy.merge(
        benchmark,
        on="date",
        how="inner"
    )


    df["excess"]=(

        df["strategy"]
        /
        df["benchmark"]

    )


    print(
        "比较记录:",
        len(df)
    )


    return df



# ============================================================
# 年度收益
# ============================================================


def annual(df):


    df=df.copy()


    df["year"]=(
        df["date"]
        .dt.year
    )


    result=(

        df
        .groupby(
            "year"
        )
        .last()

    )


    result["strategy_return"]=(

        result["strategy"]
        /
        result["strategy"].shift(1)
        -
        1

    )


    result["benchmark_return"]=(

        result["benchmark"]
        /
        result["benchmark"].shift(1)
        -
        1

    )


    result["excess_return"]=(

        result["strategy_return"]
        -
        result["benchmark_return"]

    )


    return result[
        [
            "strategy_return",
            "benchmark_return",
            "excess_return"
        ]
    ]



# ============================================================
# 绘图
# ============================================================


def plot(df):


    plt.figure(
        figsize=(12,6)
    )


    plt.plot(
        df["date"],
        df["strategy"],
        label="Strategy"
    )


    plt.plot(
        df["date"],
        df["benchmark"],
        label="HS300"
    )


    plt.title(
        "Strategy vs HS300"
    )


    plt.xlabel(
        "Date"
    )


    plt.ylabel(
        "Net Value"
    )


    plt.legend()


    plt.grid()


    plt.tight_layout()


    plt.savefig(
        "strategy_vs_benchmark.png",
        dpi=150
    )


    print(
        "图片生成:"
    )

    print(
        "strategy_vs_benchmark.png"
    )



# ============================================================
# 主程序
# ============================================================


def main():


    df=compare()


    df.to_csv(
        "strategy_vs_benchmark.csv",
        index=False
    )


    year=annual(
        df
    )


    year.to_csv(
        "annual_return.csv"
    )


    print("="*60)

    print(
        "年度收益:"
    )

    print(
        year
    )


    plot(
        df
    )


    print("="*60)

    print(
        "全部完成"
    )



if __name__=="__main__":

    main()