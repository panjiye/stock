def check_market(df):

    """
    市场环境判断

    条件:

    沪深300收盘价
    >
    MA60

    True:
        允许交易

    False:
        不交易
    """


    if len(df) < 60:

        return False


    latest = df.iloc[-1]


    if (
        latest["close"]
        >
        latest["MA60"]
    ):

        return True


    return False