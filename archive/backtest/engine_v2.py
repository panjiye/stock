import pandas as pd
import time
import os


from sqlalchemy import text

from analysis.query import engine

from backtest.portfolio import Portfolio
from backtest.broker import Broker



# =====================================================
# 参数
# =====================================================

INITIAL_CASH = 1000000


START_DATE = "2005-01-01"


RESULT_DIR = "results"





# =====================================================
# 初始化
# =====================================================

def init():

    if not os.path.exists(
        RESULT_DIR
    ):

        os.makedirs(
            RESULT_DIR
        )





# =====================================================
# 加载股票池
# =====================================================

def load_stock_pool():


    print("="*60)
    print("读取股票池")


    sql=text(
        """

        SELECT

            code,
            available_date


        FROM stock_pool


        WHERE

            available_date >= :start


        ORDER BY

            available_date


        """
    )


    with engine.connect() as conn:


        df=pd.read_sql(

            sql,

            conn,

            params={

                "start":
                START_DATE

            }

        )


    df["available_date"]=pd.to_datetime(
        df["available_date"]
    )


    print(
        "股票池记录:",
        len(df)
    )


    # ===============================
    # 转换为调仓字典
    # ===============================


    schedule={}


    for date,group in df.groupby(
        "available_date"
    ):


        schedule[date]=(
            group["code"]
            .tolist()
        )


    print(
        "调仓次数:",
        len(schedule)
    )


    return schedule






# =====================================================
# 一次性加载行情
# =====================================================

def load_prices():


    print("="*60)
    print("读取行情")


    sql=text(
        """

        SELECT

            date,
            code,
            open,
            close


        FROM daily_price_qfq


        WHERE

            date >= :start


        ORDER BY

            date


        """
    )



    with engine.connect() as conn:


        df=pd.read_sql(

            sql,

            conn,

            params={

                "start":
                START_DATE

            }

        )



    df["date"]=pd.to_datetime(
        df["date"]
    )


    print(
        "行情记录:",
        len(df)
    )



    # ==============================
    # 转换内存结构
    # ==============================


    market={}


    for date,group in df.groupby(
        "date"
    ):


        market[date]={}


        for row in group.itertuples():


            market[date][row.code]={

                "open":
                    row.open,

                "close":
                    row.close

            }



    print(
        "交易日:",
        len(market)
    )


    return market






# =====================================================
# 买入组合
# =====================================================

def buy_portfolio(
        portfolio,
        broker,
        stocks,
        prices,
        date,
        trades
):


    if len(stocks)==0:

        return



    cash = portfolio.cash



    each_cash = (

        cash /

        len(stocks)

    )



    for code in stocks:



        if code not in prices:

            continue



        price=prices[code]["open"]



        if price<=0:

            continue



        shares=broker.calculate_shares(

            each_cash,

            price

        )



        if shares<=0:

            continue



        deal_price=broker.buy_price(
            price
        )


        amount=(
            shares
            *
            deal_price
        )


        fee=broker.buy_cost(
            amount
        )


        ok=portfolio.buy(

            code,

            shares,

            deal_price,

            fee

        )


        if ok:


            trades.append(

                {

                    "date":
                    date,

                    "code":
                    code,

                    "action":
                    "BUY",

                    "price":
                    deal_price,

                    "shares":
                    shares

                }

            )





# =====================================================
# 卖出全部
# =====================================================

def sell_all(
        portfolio,
        broker,
        prices,
        date,
        trades
):


    holdings=list(

        portfolio.positions.keys()

    )


    for code in holdings:


        if code not in prices:

            continue



        price=prices[code]["close"]



        deal_price=broker.sell_price(
            price
        )



        shares=portfolio.positions[code]["shares"]



        amount=(
            shares
            *
            deal_price
        )


        fee=broker.sell_cost(
            amount
        )


        portfolio.sell(

            code,

            deal_price,

            fee

        )


        trades.append(

            {

                "date":
                date,

                "code":
                code,

                "action":
                "SELL",

                "price":
                deal_price,

                "shares":
                shares

            }

        )





# =====================================================
# 回测
# =====================================================

def run():


    start=time.time()


    init()


    schedule=load_stock_pool()


    market=load_prices()



    portfolio=Portfolio(
        INITIAL_CASH
    )


    broker=Broker()


    trades=[]


    print("="*60)
    print("开始回测")



    for date in sorted(
        market.keys()
    ):



        prices=market[date]



        # ==========================
        # 调仓
        # ==========================


        if date in schedule:


            print(

                "调仓:",

                date.strftime(
                    "%Y-%m-%d"
                )

            )


            sell_all(

                portfolio,

                broker,

                prices,

                date,

                trades

            )


            buy_portfolio(

                portfolio,

                broker,

                schedule[date],

                prices,

                date,

                trades

            )



        # ==========================
        # 每日净值
        # ==========================


        close_prices={}


        for code,value in prices.items():

            close_prices[code]=value["close"]



        portfolio.record(

            date,

            close_prices

        )





    equity=portfolio.get_history()



    equity.to_csv(

        f"{RESULT_DIR}/equity.csv",

        index=False

    )


    pd.DataFrame(

        trades

    ).to_csv(

        f"{RESULT_DIR}/trades.csv",

        index=False

    )



    print("="*60)


    print(
        "完成"
    )


    print(
        "最终资产:",
        round(
            equity.iloc[-1]["total_value"],
            2
        )
    )


    print(
        "交易次数:",
        len(trades)
    )


    print(
        "耗时:",
        round(
            time.time()-start,
            2
        ),
        "秒"
    )





if __name__=="__main__":

    run()