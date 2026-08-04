import pandas as pd
import numpy as np



def normalize_percent(value):

    """
    百分比字段标准化

    东方财富历史数据存在两种格式:

    旧:
        0.344620

        表示34.462%


    新:
        10.57

        表示10.57%


    统一输出:

        小数形式

        0.1057

    """


    if pd.isna(value):

        return np.nan


    value=float(value)


    if abs(value)>2:

        return value / 100


    return value



def normalize_financial_profit(df):

    """
    financial_profit

    转换为标准化财务数据

    """


    df=df.copy()


    result=pd.DataFrame()

    result["code"]=df["code"]

    result["pub_date"]=df["pub_date"]

    result["stat_date"]=df["stat_date"]

    # ====================
    # 百分比字段
    # ====================


    result["roe"]=(
        df["roe_avg"]
        .apply(normalize_percent)
    )


    result["net_margin"]=(
        df["np_margin"]
        .apply(normalize_percent)
    )


    result["gross_margin"]=(
        df["gp_margin"]
        .apply(normalize_percent)
    )



    # ====================
    # 金融数据
    # ====================


    result["net_profit"]=(
        df["net_profit"]
    )


    result["eps"]=(
        df["eps_ttm"]
    )


    result["revenue"]=(
        df["main_business_revenue"]
    )


    return result