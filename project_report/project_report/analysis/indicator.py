import pandas as pd



def add_ma(df):

    """
    添加均线指标

    MA5
    MA10
    MA20
    MA60
    """


    df = df.copy()


    df["MA5"] = (
        df["close"]
        .rolling(5)
        .mean()
    )


    df["MA10"] = (
        df["close"]
        .rolling(10)
        .mean()
    )


    df["MA20"] = (
        df["close"]
        .rolling(20)
        .mean()
    )


    df["MA60"] = (
        df["close"]
        .rolling(60)
        .mean()
    )


    return df

def add_macd(df):

    """
    添加MACD指标

    DIF
    DEA
    MACD柱
    """

    df = df.copy()


    ema12 = (
        df["close"]
        .ewm(
            span=12,
            adjust=False
        )
        .mean()
    )


    ema26 = (
        df["close"]
        .ewm(
            span=26,
            adjust=False
        )
        .mean()
    )


    df["DIF"] = ema12 - ema26


    df["DEA"] = (
        df["DIF"]
        .ewm(
            span=9,
            adjust=False
        )
        .mean()
    )


    df["MACD"] = (
        (df["DIF"] - df["DEA"])
        * 2
    )


    return df

def add_rsi(df, period=14):

    """
    RSI指标
    """

    df = df.copy()


    delta = df["close"].diff()


    gain = delta.where(
        delta > 0,
        0
    )


    loss = -delta.where(
        delta < 0,
        0
    )


    avg_gain = (
        gain
        .rolling(period)
        .mean()
    )


    avg_loss = (
        loss
        .rolling(period)
        .mean()
    )


    rs = avg_gain / avg_loss


    df["RSI"] = (
        100 -
        (100/(1+rs))
    )


    return df

def add_kdj(df, n=9):

    """
    KDJ指标
    """

    df = df.copy()


    low_min = (
        df["low"]
        .rolling(n)
        .min()
    )


    high_max = (
        df["high"]
        .rolling(n)
        .max()
    )


    rsv = (
        (df["close"] - low_min)
        /
        (high_max-low_min)
        *100
    )


    df["K"] = (
        rsv
        .ewm(
            com=2
        )
        .mean()
    )


    df["D"] = (
        df["K"]
        .ewm(
            com=2
        )
        .mean()
    )


    df["J"] = (
        3*df["K"]
        -
        2*df["D"]
    )


    return df

def add_indicator(df):

    """
    添加全部技术指标

    MA
    MACD
    RSI
    KDJ
    """

    df = add_ma(df)

    df = add_macd(df)

    df = add_rsi(df)

    df = add_kdj(df)

    return df