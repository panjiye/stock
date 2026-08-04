import pandas as pd
import numpy as np

def roe_score(x):

    if pd.isna(x):
        return 0


    if x < 0:
        return 0


    if x < 0.1:
        return 0.5


    if x < 0.3:
        return 1


    if x < 0.5:
        return 0.8


    return 0.5

def add_growth_factor(df):

    """
    计算同比增长

    profit_growth
    revenue_growth

    """

    df = df.copy()


    df["stat_date"] = pd.to_datetime(
        df["stat_date"]
    )


    last_year = df[
        [
            "code",
            "stat_date",
            "net_profit",
            "revenue"
        ]
    ].copy()


    #
    # 日期向后移动一年
    #
    last_year["stat_date"] = (
        last_year["stat_date"]
        +
        pd.DateOffset(
            years=1
        )
    )


    last_year.rename(
        columns={

            "net_profit":
                "last_year_profit",

            "revenue":
                "last_year_revenue"

        },
        inplace=True
    )


    df = df.merge(

        last_year,

        on=[
            "code",
            "stat_date"
        ],

        how="left"

    )


    df["profit_growth"] = (

        df["net_profit"]
        -
        df["last_year_profit"]

    ) / df["last_year_profit"].abs()



    df["revenue_growth"] = (

        df["revenue"]
        -
        df["last_year_revenue"]

    ) / df["last_year_revenue"].abs()



    df["profit_growth"] = (
        df["profit_growth"]
        .replace(
            [np.inf,-np.inf],
            np.nan
        )
    )


    df["revenue_growth"] = (
        df["revenue_growth"]
        .replace(
            [np.inf,-np.inf],
            np.nan
        )
    )


    return df



def add_quality_factor(df):

    """
    财务质量因子

    """

    df=df.copy()


    #
    # ROE限制
    #
    # 防止历史异常数据污染评分
    #
    df["roe_clip"] = (
        df["roe"]
        .clip(
            -1,
            1
        )
    )


    #
    # 增长限制
    #
    df["profit_growth"] = (
        df["profit_growth"]
        .clip(
            -1,
            3
        )
    )


    df["revenue_growth"] = (
        df["revenue_growth"]
        .clip(
            -1,
            3
        )
    )


    #
    # 增长质量
    #
    df["growth_quality"]=(

        df["profit_growth"]
        *
        0.6

        +

        df["revenue_growth"]
        *
        0.4

    )


    #
    # 盈利稳定性
    #
    df=df.sort_values(
        [
            "code",
            "stat_date"
        ]
    )


    growth_std=(

        df
        .groupby("code")
        ["profit_growth"]
        .rolling(
            4,
            min_periods=2
        )
        .std()

    )


    growth_std = (
        growth_std
        .reset_index(
            level=0,
            drop=True
        )
    )


    df["stability_score"]=(

        1 /
        (
            1+
            growth_std.abs()
        )

    )


    #
    # 综合质量评分
    #
    df["quality_score"]=(

        df["roe_clip"]
        .fillna(0)
        *
        0.5


        +

        df["growth_quality"]
        .fillna(0)
        *
        0.3


        +

        df["stability_score"]
        .fillna(0)
        *
        0.2

    )


    return df



def calculate_financial_factor(df):

    """
    财务因子主入口

    输入:
        financial_profit_normalized

    输出:
        financial_factor

    """


    df=df.copy()


    df=df.sort_values(
        [
            "code",
            "stat_date"
        ]
    )


    #
    # 增长
    #
    df=add_growth_factor(
        df
    )


    #
    # 质量
    #
    df=add_quality_factor(
        df
    )


    result=pd.DataFrame()

    result["code"]=df["code"]
    
    result["pub_date"]=(
        pd.to_datetime(
            df["pub_date"],
            errors="coerce",
            format="mixed"
        )
        .dt.strftime(
            "%Y-%m-%d"
        )
    )
    
    result["stat_date"]=(
        df["stat_date"]
        .dt.strftime(
            "%Y-%m-%d"
        )
    )


    result["roe_score"]=(
        df["roe"]
        .apply(
            roe_score
        )
    )
    
    result["roe_clip"]=df["roe_clip"]


    result["net_margin"]=df["net_margin"]


    result["gross_margin"]=df["gross_margin"]


    result["eps"]=df["eps"]


    result["profit_growth"]=(
        df["profit_growth"]
    )


    result["revenue_growth"]=(
        df["revenue_growth"]
    )


    result["growth_quality"]=(
        df["growth_quality"]
    )


    result["stability_score"]=(
        df["stability_score"]
    )


    result["quality_score"]=(

        result["roe_score"]
        *
        0.35


        +

        result["growth_quality"]
        .fillna(0)
        *
        0.25


        +

        df["stability_score"]
        .fillna(0)
        *
        0.25


        +

        result["net_margin"]
        .fillna(0)
        *
        0.15

    )


    return result