def calculate_strategy_return(
    final_cash,
    initial_cash=100000
):

    """
    计算策略收益率
    """

    return round(
        (
            final_cash
            -
            initial_cash
        )
        /
        initial_cash
        *
        100,

        2
    )