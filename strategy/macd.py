import pandas as pd


def check_macd(df):

    """
    MACD 多头判断

    条件:
    DIF > DEA
    MACD > 0

    返回:
    True / False
    """

    if len(df) < 2:
        return False


    latest = df.iloc[-1]


    if (
        latest["DIF"] > latest["DEA"]
        and latest["MACD"] > 0
    ):
        return True

    return False