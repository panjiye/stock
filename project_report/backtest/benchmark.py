def calculate_benchmark(df):

    """
    计算基准收益

    默认:
    买入第一天
    持有到最后一天

    """

    if len(df) == 0:
        return None


    start_price = float(
        df.iloc[0]["close"]
    )


    end_price = float(
        df.iloc[-1]["close"]
    )


    return round(
        (
            end_price
            -
            start_price
        )
        /
        start_price
        *
        100,

        2
    )