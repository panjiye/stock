import pandas as pd


def summarize(results):

    """
    汇总回测结果
    """

    df = pd.DataFrame(results)


    print("================")
    print("回测统计")
    print("================")


    print(
        "信号数量:",
        len(df)
    )


    for col in [
        "return_5",
        "return_10",
        "return_20"
    ]:


        data = (
            df[col]
            .dropna()
        )


        win = (
            data > 0
        ).sum()


        total = len(data)


        print()

        print(
            col
        )


        print(
            "有效次数:",
            total
        )


        print(
            "平均收益:",
            round(
                data.mean(),
                2
            ),
            "%"
        )


        print(
            "胜率:",
            round(
                win / total * 100,
                2
            ),
            "%"
        )