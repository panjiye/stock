# scripts/backtest_factor.py

"""
季度多因子组合回测

逻辑：

factor_score
        |
        | 每季度 final_score 排序
        |
        v
TOP100
        |
        | 下一交易日 open 买入
        |
        v
持有一个季度
        |
        v
季度最后交易日 close 卖出


版本:
v2

特点:
1. 使用真实factor_score排序
2. 避免未来函数
3. 交易日缓存
4. 支持大数据SQLite
"""


import os
import json
import bisect

import pandas as pd

from sqlalchemy import text

from analysis.query import engine



# ==================================================
# 参数
# ==================================================

INITIAL_CAPITAL = 1000000

TOP_N = 100


START_DATE = "2010-01-01"


RESULT_DIR = "backtest_result"



os.makedirs(
    RESULT_DIR,
    exist_ok=True
)



# ==================================================
# 全局交易日缓存
# ==================================================

TRADE_DATES = []



# ==================================================
# 加载交易日历
# ==================================================

def load_trade_calendar():


    global TRADE_DATES


    print("=" * 60)
    print("读取交易日历...")


    sql = """
    SELECT DISTINCT date

    FROM daily_price_qfq

    ORDER BY date
    """


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn
        )


    TRADE_DATES = (
        pd.to_datetime(df["date"])
        .dt.strftime("%Y-%m-%d")
        .tolist()
    )


    print(
        "交易日数量:",
        len(TRADE_DATES)
    )



# ==================================================
# 获取下一交易日
# ==================================================

def next_trade_day(date):


    index = bisect.bisect_right(
        TRADE_DATES,
        date
    )


    if index >= len(TRADE_DATES):

        return None


    return TRADE_DATES[index]



# ==================================================
# 获取区间最后交易日
# ==================================================

def last_trade_day(
        start,
        end
):


    index = bisect.bisect_right(
        TRADE_DATES,
        end
    )


    index -= 1


    if index < 0:

        return None


    return TRADE_DATES[index]



# ==================================================
# 读取季度因子股票池
# ==================================================

def load_factor_pool():


    print("=" * 60)

    print(
        "读取因子数据..."
    )


    sql = """
    SELECT

        f.code,

        f.stat_date,

        f.final_score


    FROM factor_score f


    WHERE f.stat_date >= :start


    ORDER BY

        f.stat_date,

        f.final_score DESC

    """


    with engine.connect() as conn:

        df = pd.read_sql(
            text(sql),
            conn,
            params={
                "start":START_DATE
            }
        )



    df["stat_date"] = (

        pd.to_datetime(
            df["stat_date"]
        )
        .dt.strftime("%Y-%m-%d")

    )


    print(
        "因子记录:",
        len(df)
    )


    print(
        "季度数量:",
        df["stat_date"]
        .nunique()
    )


    return df



# ==================================================
# 读取股票池过滤
# ==================================================

def load_stock_enable():


    print(
        "读取股票过滤信息..."
    )


    sql="""

    SELECT

        code,

        stat_date


    FROM stock_pool


    WHERE enable=1

    """


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    df["stat_date"]=(

        pd.to_datetime(
            df["stat_date"]
        )
        .dt.strftime("%Y-%m-%d")

    )


    print(
        "有效股票:",
        len(df)
    )


    return df



# ==================================================
# 每季度选择股票
# ==================================================

def select_stocks(
        factor_df,
        enable_df,
        date
):


    df = factor_df[

        factor_df["pub_date"]
        <=
        date

    ]


    if len(df)==0:

        return []



    enable = enable_df[

        enable_df["stat_date"]
        ==
        date

    ]



    df=df.merge(

        enable[["code"]],

        on="code",

        how="inner"

    )


    df=df.sort_values(

        "final_score",

        ascending=False

    )



    stocks=(

        df.head(TOP_N)
        ["code"]
        .tolist()

    )


    return stocks



# ==================================================
# 查询买入价格
# ==================================================

def get_open_price(
        codes,
        date
):


    if len(codes)==0:

        return pd.DataFrame()



    params={

        "date":date

    }


    holders=[]


    for i,code in enumerate(codes):

        key=f"code{i}"

        holders.append(
            ":"+key
        )

        params[key]=code



    sql=text(
        f"""

        SELECT

            code,

            open


        FROM daily_price_qfq


        WHERE date=:date


        AND code IN
        (
            {",".join(holders)}
        )

        """
    )



    with engine.connect() as conn:


        df=pd.read_sql(

            sql,

            conn,

            params=params

        )


    return df

# ==================================================
# 查询卖出价格
# ==================================================

def get_close_price(
        codes,
        date
):


    if len(codes)==0:

        return pd.DataFrame()



    params={

        "date":date

    }


    holders=[]


    for i,code in enumerate(codes):

        key=f"code{i}"

        holders.append(
            ":"+key
        )

        params[key]=code



    sql=text(
        f"""

        SELECT

            code,

            close


        FROM daily_price_qfq


        WHERE date=:date


        AND code IN
        (
            {",".join(holders)}
        )


        """
    )



    with engine.connect() as conn:


        df=pd.read_sql(

            sql,

            conn,

            params=params

        )


    return df




# ==================================================
# 回测主程序
# ==================================================

def run_backtest(
        factor_df,
        enable_df
):


    print("="*60)

    print(
        "开始季度多因子回测"
    )


    dates=sorted(

        factor_df["stat_date"]
        .unique()

    )


    print(

        "回测季度:",

        len(dates)

    )


    cash=INITIAL_CAPITAL


    equity=[]


    trades=[]



    for i in range(
        len(dates)-1
    ):


        rebalance_date=dates[i]


        next_period=dates[i+1]



        print()
        print(
            "="*40
        )

        print(
            "调仓日期:",
            rebalance_date
        )



        # --------------------------
        # 选股
        # --------------------------

        stocks=select_stocks(

            factor_df,

            enable_df,

            rebalance_date

        )


        print(

            "入选股票:",

            len(stocks)

        )


        if len(stocks)==0:

            continue



        # --------------------------
        # 买入日期
        # --------------------------

        buy_date=next_trade_day(

            rebalance_date

        )


        if buy_date is None:

            continue



        print(

            "买入日期:",

            buy_date

        )



        price=get_open_price(

            stocks,

            buy_date

        )



        if len(price)==0:

            print(
                "无买入价格"
            )

            continue



        # --------------------------
        # 建仓
        # --------------------------

        holdings={}


        amount_per_stock=(

            cash

            /

            len(price)

        )



        for _,row in price.iterrows():


            code=row["code"]


            open_price=float(

                row["open"]

            )


            shares=(

                amount_per_stock

                /

                open_price

            )


            holdings[code]={

                "buy_date":
                buy_date,


                "buy_price":
                open_price,


                "shares":
                shares

            }



        # --------------------------
        # 卖出日期
        # --------------------------

        sell_date=last_trade_day(

            buy_date,

            next_period

        )


        if sell_date is None:

            continue



        close=get_close_price(

            list(holdings.keys()),

            sell_date

        )



        if len(close)==0:

            continue



        total_value=0



        for _,row in close.iterrows():


            code=row["code"]


            close_price=float(

                row["close"]

            )


            h=holdings[code]


            value=(

                h["shares"]

                *

                close_price

            )


            total_value += value



            trades.append(

                {

                "buy_date":
                h["buy_date"],


                "sell_date":
                sell_date,


                "code":
                code,


                "buy_price":
                h["buy_price"],


                "sell_price":
                close_price,


                "return":

                close_price
                /
                h["buy_price"]
                -
                1

                }

            )



        cash=total_value



        equity.append(

            {

            "date":
            sell_date,


            "value":
            cash

            }

        )



        print(

            "卖出日期:",

            sell_date,

            "资产:",

            round(
                cash,
                2
            )

        )



    return equity,trades





# ==================================================
# 性能计算
# ==================================================

def calculate_performance(
        equity_df
):


    if len(equity_df)==0:

        return {}



    start_value=float(

        equity_df.iloc[0]["value"]

    )


    end_value=float(

        equity_df.iloc[-1]["value"]

    )



    total_return=(

        end_value

        /

        start_value

        -
        1

    )



    years=(

        len(equity_df)

        /

        4

    )



    annual_return=(

        (end_value/start_value)

        **

        (1/years)

        -
        1

    )



    equity_df["high"]= (

        equity_df["value"]

        .cummax()

    )


    equity_df["drawdown"]=(

        equity_df["value"]

        /

        equity_df["high"]

        -
        1

    )



    max_drawdown=float(

        equity_df["drawdown"]

        .min()

    )



    return {


        "initial_capital":

        INITIAL_CAPITAL,


        "final_value":

        end_value,


        "total_return":

        total_return,


        "annual_return":

        annual_return,


        "max_drawdown":

        max_drawdown


    }





# ==================================================
# main
# ==================================================

if __name__=="__main__":


    load_trade_calendar()



    factor_df=load_factor_pool()



    enable_df=load_stock_enable()



    equity,trades=run_backtest(

        factor_df,

        enable_df

    )



    equity_df=pd.DataFrame(

        equity

    )


    trade_df=pd.DataFrame(

        trades

    )



    equity_df.to_csv(

        f"{RESULT_DIR}/equity_curve.csv",

        index=False

    )



    trade_df.to_csv(

        f"{RESULT_DIR}/trade_log.csv",

        index=False

    )



    performance=calculate_performance(

        equity_df

    )



    with open(

        f"{RESULT_DIR}/performance.json",

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            performance,

            f,

            indent=4,

            ensure_ascii=False

        )



    print()

    print("="*60)

    print(
        "回测完成"
    )


    print(

        json.dumps(

            performance,

            indent=4,

            ensure_ascii=False

        )

    )