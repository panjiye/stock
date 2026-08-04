def generate_benchmark_report(
    strategy_return,
    benchmark_return
):

    excess_return = (
        strategy_return
        -
        benchmark_return
    )


    print("================")
    print("策略 VS 沪深300")
    print("================")


    print(
        "策略收益:",
        strategy_return,
        "%"
    )


    print(
        "沪深300:",
        benchmark_return,
        "%"
    )


    print(
        "超额收益:",
        round(excess_return,2),
        "%"
    )