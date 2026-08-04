import pandas as pd



def calculate_future_return(df, index):

    """
    计算信号后的未来收益


    参数:

    df:
        股票完整行情


    index:
        买入信号所在位置


    返回:

    5日
    10日
    20日收益

    """



    result = {

        "return_5": None,

        "return_10": None,

        "return_20": None

    }



    buy_price = df.iloc[index]["close"]



    periods = {

        "return_5":5,

        "return_10":10,

        "return_20":20

    }



    for key,days in periods.items():


        future_index = index + days



        # 数据不足

        if future_index >= len(df):

            continue



        future_price = (
            df.iloc[future_index]["close"]
        )


        result[key] = round(
            (
                future_price
                -
                buy_price
            )
            /
            buy_price
            *
            100,

            2
        )


    return result