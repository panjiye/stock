import pandas as pd
import numpy as np



def clip_value(
        series,
        low,
        high
):

    return (
        series
        .clip(
            lower=low,
            upper=high
        )
    )



def add_clip_factor(df):

    df=df.copy()


    #
    # ROE限制
    #
    df["roe_clip"]=clip_value(
        df["roe"],
        -1,
        1
    )


    #
    # 增长率限制
    #
    df["profit_growth_clip"]=clip_value(
        df["profit_growth"],
        -2,
        5
    )


    df["revenue_growth_clip"]=clip_value(
        df["revenue_growth"],
        -2,
       5
    )


    return df




def add_stability_factor(df):

    """
    盈利稳定性

    使用:
    最近4季度增长波动

    """

    df=df.copy()


    df=df.sort_values(
        [
            "code",
            "stat_date"
        ]
    )


    df["growth_std"]=(
        df
        .groupby("code")
        ["profit_growth"]
        .rolling(
            4,
            min_periods=2
        )
        .std()
        .reset_index(
            level=0,
            drop=True
        )
    )


    #
    # 波动越小越好
    #
    df["stability_score"]=(
        1 /
        (
            1+
            df["growth_std"].abs()
        )
    )


    return df



def add_quality_score(df):

    df=df.copy()


    df["quality_score"]=(
        df["roe_clip"].fillna(0)*0.4
        +
        df["stability_score"].fillna(0)*0.3
        +
        df["gross_margin"].fillna(0)*0.3
    )


    return df




def build_quality(df):

    df=add_clip_factor(df)

    df=add_stability_factor(df)

    df=add_quality_score(df)

    return df