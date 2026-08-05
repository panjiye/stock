def generate_report(trades):

    print("================")
    print("回测报告")
    print("================")


    total = len(trades)


    if total == 0:

        print("没有交易")

        return



    profits = []


    losses = []


    returns = []


    for t in trades:


        r = t["return"]


        returns.append(r)


        if r > 0:

            profits.append(r)

        else:

            losses.append(r)



    win_count = len(profits)


    loss_count = len(losses)



    win_rate = (
        win_count / total * 100
    )



    avg_return = (
        sum(returns)
        /
        total
    )



    avg_profit = 0

    if profits:

        avg_profit = (
            sum(profits)
            /
            len(profits)
        )



    avg_loss = 0

    if losses:

        avg_loss = (
            sum(losses)
            /
            len(losses)
        )



    max_profit = max(returns)


    max_loss = min(returns)



    total_return = sum(returns)



    print()

    print(
        "交易次数:",
        total
    )


    print(
        "盈利次数:",
        win_count
    )


    print(
        "亏损次数:",
        loss_count
    )


    print(
        "胜率:",
        round(win_rate,2),
        "%"
    )


    print(
        "平均收益:",
        round(avg_return,2),
        "%"
    )


    print(
        "平均盈利:",
        round(avg_profit,2),
        "%"
    )


    print(
        "平均亏损:",
        round(avg_loss,2),
        "%"
    )


    print(
        "最大盈利:",
        round(max_profit,2),
        "%"
    )


    print(
        "最大亏损:",
        round(max_loss,2),
        "%"
    )


    print(
        "累计收益:",
        round(total_return,2),
        "%"
    )