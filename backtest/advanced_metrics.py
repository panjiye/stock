import pandas as pd
import numpy as np


# =========================================================
# 基础收益序列
# =========================================================

def calculate_returns(
    df,
    value_col
):

    df = df.copy()

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = df.sort_values(
        "date"
    )

    df["return"] = (
        df[value_col]
        .pct_change()
    )

    return df



# =========================================================
# Alpha Beta
# =========================================================

def calculate_alpha_beta(
    strategy,
    benchmark
):

    """
    CAPM:

    Rp = alpha + beta * Rm

    """

    s = calculate_returns(
        strategy,
        "total_value"
    )


    b = calculate_returns(
        benchmark,
        "value"
    )


    df = pd.merge(
        s[
            [
                "date",
                "return"
            ]
        ],

        b[
            [
                "date",
                "return"
            ]
        ],

        on="date",

        suffixes=(
            "_strategy",
            "_market"
        )
    )


    df = df.dropna()


    if len(df)<10:

        return {
            "alpha":0,
            "beta":0
        }



    x = df["return_market"]

    y = df["return_strategy"]



    beta = (
        np.cov(
            x,
            y
        )[0][1]
        /
        np.var(x)
    )


    alpha_daily = (
        y.mean()
        -
        beta*x.mean()
    )


    alpha_year = (
        alpha_daily
        *
        250
        *
        100
    )


    return {

        "alpha":
            round(alpha_year,2),

        "beta":
            round(beta,2)

    }




# =========================================================
# 超额收益
# =========================================================

def calculate_excess_return(
    strategy,
    benchmark
):


    s = strategy.copy()

    b = benchmark.copy()


    s["date"] = pd.to_datetime(
        s["date"]
    )

    b["date"] = pd.to_datetime(
        b["date"]
    )



    df = pd.merge(
        s[
            [
                "date",
                "total_value"
            ]
        ],

        b[
            [
                "date",
                "value"
            ]
        ],

        on="date"
    )


    df = df.sort_values(
        "date"
    )



    df["strategy_nav"] = (
        df["total_value"]
        /
        df["total_value"].iloc[0]
    )


    df["benchmark_nav"] = (
        df["value"]
        /
        df["value"].iloc[0]
    )


    df["excess_nav"] = (
        df["strategy_nav"]
        /
        df["benchmark_nav"]
    )



    return df[
        [
            "date",
            "strategy_nav",
            "benchmark_nav",
            "excess_nav"
        ]
    ]




# =========================================================
# 最大回撤区间
# =========================================================

def calculate_drawdown_period(
    df,
    value_col
):


    df = df.copy()


    df["date"] = pd.to_datetime(
        df["date"]
    )


    df = df.sort_values(
        "date"
    )


    values = df[value_col]


    high = values.cummax()


    drawdown = (
        values /
        high
        -
        1
    )


    end_index = (
        drawdown
        .idxmin()
    )


    max_dd = drawdown.loc[
        end_index
    ]



    peak_index = (
        values.loc[:end_index]
        .idxmax()
    )



    return {

        "start":
            df.loc[
                peak_index,
                "date"
            ],

        "end":
            df.loc[
                end_index,
                "date"
            ],

        "drawdown":
            round(
                max_dd*100,
                2
            )

    }




# =========================================================
# 年度收益
# =========================================================

def yearly_return(
    df,
    value_col
):


    data=df.copy()


    data["date"]=pd.to_datetime(
        data["date"]
    )


    data=data.sort_values(
        "date"
    )


    data["year"] = (
        data["date"]
        .dt.year
    )


    result=[]


    for year,g in data.groupby(
        "year"
    ):


        start=g[value_col].iloc[0]

        end=g[value_col].iloc[-1]


        ret=(
            end/start-1
        )*100


        result.append(
            {
                "year":
                    year,

                "return":
                    round(ret,2)

            }
        )


    return pd.DataFrame(
        result
    )




# =========================================================
# 月度收益
# =========================================================

def monthly_return(
    df,
    value_col
):


    data=df.copy()


    data["date"]=pd.to_datetime(
        data["date"]
    )


    data=data.sort_values(
        "date"
    )


    data["month"]=(
        data["date"]
        .dt.to_period("M")
    )



    result=[]


    for month,g in data.groupby(
        "month"
    ):


        start=g[value_col].iloc[0]

        end=g[value_col].iloc[-1]


        ret=(
            end/start-1
        )*100


        result.append(
            {
                "month":
                    str(month),

                "return":
                    round(ret,2)

            }
        )


    return pd.DataFrame(
        result
    )