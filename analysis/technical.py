import pandas as pd
import numpy as np



def add_ma(df):

    df=df.copy()


    df["ma20"]=(

        df.groupby("code")["close"]

        .transform(
            lambda x:
            x.rolling(20).mean()
        )

    )


    df["ma60"]=(

        df.groupby("code")["close"]

        .transform(
            lambda x:
            x.rolling(60).mean()
        )

    )


    df["ma120"]=(

        df.groupby("code")["close"]

        .transform(
            lambda x:
            x.rolling(120).mean()
        )

    )


    return df




def add_return(df):

    df=df.copy()


    g=df.groupby("code")["close"]


    df["return20"]=(

        g.shift(0)

        /

        g.shift(20)

        -1

    )


    df["return60"]=(

        g.shift(0)

        /

        g.shift(60)

        -1

    )


    df["return120"]=(

        g.shift(0)

        /

        g.shift(120)

        -1

    )


    return df




def add_volatility(df):


    df=df.copy()


    df["daily_return"]=(

        df.groupby("code")["close"]

        .pct_change()

    )


    df["volatility"]=(

        df.groupby("code")["daily_return"]

        .transform(

            lambda x:
            x.rolling(20)
            .std()

            *

            np.sqrt(252)

        )

    )


    return df




def add_score(df):


    df=df.copy()


    #
    # 趋势评分
    #

    df["trend_score"]=0


    df.loc[

        (
        df["close"]>df["ma20"]
        )

        &

        (
        df["ma20"]>df["ma60"]
        )

        &

        (
        df["ma60"]>df["ma120"]
        ),

        "trend_score"

    ]=1



    #
    # 动量评分
    #

    df["momentum_score"]=(

        df["return20"].rank(
            pct=True
        )

        *

        0.4

        +

        df["return60"].rank(
            pct=True
        )

        *

        0.3

        +

        df["return120"].rank(
            pct=True
        )

        *

        0.3

    )



    #
    # 稳定性
    #

    stability=(

        1-df["volatility"]

    )


    stability=(

        stability.clip(
            0,
            1
        )

    )


    df["technical_score"]=(

        df["trend_score"]
        *
        0.5

        +

        df["momentum_score"]
        *
        0.3

        +

        stability
        *
        0.2

    )


    return df




def build_technical(df):


    df=df.copy()


    df=df.sort_values(

        [
            "code",
            "date"
        ]

    )


    df=add_ma(df)


    df=add_return(df)


    df=add_volatility(df)


    df=add_score(df)


    return df