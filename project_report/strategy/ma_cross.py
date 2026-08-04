def check_ma_cross(df):

    """
    MA5 金叉 MA20

    昨天:
    MA5 < MA20

    今天:
    MA5 > MA20

    返回:
    True 买入
    """

    if len(df) < 20:
        return False


    yesterday = df.iloc[-2]

    today = df.iloc[-1]


    if (
        yesterday["MA5"]
        <
        yesterday["MA20"]

        and

        today["MA5"]
        >
        today["MA20"]
    ):

        return True


    return False

def find_ma_cross(df):

    """
    找出所有MA金叉日期
    """

    signals = []


    for i in range(1,len(df)):


        yesterday = df.iloc[i-1]

        today = df.iloc[i]


        if (
            yesterday["MA5"]
            <
            yesterday["MA20"]

            and

            today["MA5"]
            >
            today["MA20"]
        ):

            signals.append(
                today["date"]
            )


    return signals