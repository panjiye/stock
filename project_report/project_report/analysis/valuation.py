import pandas as pd
import numpy as np



def calculate_pe(df):

    df=df.copy()


    df["pe"] = (

        df["close"]

        /

        df["eps"]

    )


    df["pe"]=(

        df["pe"]

        .replace(
            [np.inf,-np.inf],
            np.nan
        )

    )


    return df




def add_pe_rank(df):

    """

    股票自身历史PE分位

    """

    df=df.sort_values(
        [
            "code",
            "stat_date"
        ]
    )


    def rank(group):

        return (
            group["pe"]
            .rank(
                pct=True
            )
        )


    df["pe_rank"]=(

        df.groupby(
            "code",
            group_keys=False
        )
        .apply(
            rank
        )

        .reset_index(
            drop=True
        )

    )


    return df




def calculate_valuation_score(df):


    df=df.copy()


    df["valuation_score"]=(

        1

        -

        df["pe_rank"]

    )


    return df




def build_valuation(df):


    df=df.copy()


    df=calculate_pe(
        df
    )


    df=add_pe_rank(
        df
    )


    df=calculate_valuation_score(
        df
    )


    return df