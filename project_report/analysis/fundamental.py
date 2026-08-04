import sqlite3
import pandas as pd
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DB_PATH = os.path.join(
    BASE_DIR,
    "database",
    "stock.db"
)



def get_connection():

    return sqlite3.connect(DB_PATH)

def check_financial_quality(code):

    conn = get_connection()


    sql = """

    SELECT

    count(*) as cnt,

    max(stat_date) as latest


    FROM financial_profit

    WHERE code=?

    """


    df = pd.read_sql(
        sql,
        conn,
        params=(code,)
    )


    conn.close()


    if df.empty:
        return False


    cnt = df.iloc[0]["cnt"]

    latest = df.iloc[0]["latest"]


    if cnt < 8:
        return False


    if latest < "2025-12-31":
        return False


    return True

# ==========================
# 获取最新财务数据
# ==========================

def get_latest_financial(code):


    conn = get_connection()


    sql = """
    SELECT
        code,
        stat_date,
        roe_avg,
        np_margin,
        gp_margin,
        net_profit,
        eps_ttm,
        main_business_revenue

    FROM financial_profit

    WHERE code = ?

    ORDER BY stat_date DESC

    LIMIT 1

    """


    df = pd.read_sql(
        sql,
        conn,
        params=(code,)
    )


    conn.close()


    if df.empty:

        return None



    row = df.iloc[0]


    return {

        "code": row["code"],

        "date": row["stat_date"],

        "roe": row["roe_avg"],

        "net_margin": row["np_margin"],

        "gross_margin": row["gp_margin"],

        "profit": row["net_profit"],

        "eps": row["eps_ttm"],

        "revenue": row["main_business_revenue"]

    }





# ==========================
# 历史财务
# ==========================


def get_financial_history(code):


    conn = get_connection()


    sql = """

    SELECT *

    FROM financial_profit

    WHERE code=?

    ORDER BY stat_date

    """


    df = pd.read_sql(
        sql,
        conn,
        params=(code,)
    )


    conn.close()


    return df





# ==========================
# 利润增长率
# ==========================


def get_profit_growth(code):


    df = get_financial_history(code)


    if len(df) < 2:

        return None



    latest = df.iloc[-1]

    previous = df.iloc[-2]



    if previous["net_profit"] == 0:

        return None



    growth = (

        latest["net_profit"]

        /

        previous["net_profit"]

        -

        1

    ) * 100



    return round(
        growth,
        2
    )





# ==========================
# 基本面评分
# ==========================


def fundamental_score(code):

    if not check_financial_quality(code):

        return {
            "score":0,
            "detail":{
                "财务数据不足":0
            },
            "growth":None
        }

    data = get_latest_financial(code)


    if data is None:

        return 0



    score = 0



    detail = {}



    # ROE

    roe = data["roe"]


    if roe >= 0.20:

        score += 30

        detail["ROE"] = 30


    elif roe >= 0.10:

        score += 20

        detail["ROE"] = 20


    else:

        detail["ROE"] = 0





    # 净利润率

    margin = data["net_margin"]


    if margin >= 0.20:

        score += 20

        detail["利润率"] = 20


    elif margin >= 0.10:

        score += 10

        detail["利润率"] = 10


    else:

        detail["利润率"] = 0





    # 净利润规模

    profit = data["profit"]


    if profit >= 1e10:

        score += 20

        detail["利润规模"] = 20


    elif profit >= 1e9:

        score += 10

        detail["利润规模"] = 10


    else:

        detail["利润规模"] = 0





    # 利润增长

    growth = get_profit_growth(code)


    if growth is not None:


        if growth > 20:

            score += 30

            detail["利润增长"] = 30


        elif growth > 0:

            score += 15

            detail["利润增长"] = 15


        else:

            detail["利润增长"] = 0


    else:

        detail["利润增长"] = 0




    return {

        "score":score,

        "detail":detail,

        "growth":growth

    }
    
