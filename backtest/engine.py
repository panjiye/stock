# 结果出来了，这一版 v4.1 风险控制有效，而且效果比较符合预期。

# 我们先和 Baseline 对比：

# 指标	v3.2 原策略	v4.1 风控策略	变化
# 最终资产	11,942,627	9,974,384	↓ 16.5%
# 累计收益	1103.18%	899.22%	↓
# 年化收益	12.22%	11.25%	↓ 0.97%
# 最大回撤	-73.61%	-57.42%	✅ 降低 16.2%
# Beta	0.98	0.77	✅ 降低风险暴露
# 波动率	29.55%	25.11%	✅ 降低
# Sharpe	0.43	0.46	✅ 提升



import os
import time
import pandas as pd
from sqlalchemy import text

from data.query import engine

from backtest.portfolio import Portfolio
from backtest.broker import Broker
from backtest.risk import MarketRisk



# ============================================================
# 参数
# ============================================================

INITIAL_CASH = 1000000

START_DATE = "2005-01-01"

RESULT_DIR = "results"


os.makedirs(
    RESULT_DIR,
    exist_ok=True
)



# ============================================================
# 初始化
# ============================================================

portfolio = Portfolio(
    INITIAL_CASH
)


broker = Broker()

# 市场风险控制
risk = MarketRisk()


trades = []


rebalance_log = []





# ============================================================
# 加载股票池
# ============================================================

def load_stock_pool():

    print(
        "读取股票池..."
    )


    sql = text(
        """
        SELECT

            code,

            pool_date,

            available_date


        FROM stock_pool


        WHERE enable=1

        """
    )


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn
        )


    df["pool_date"] = pd.to_datetime(
        df["pool_date"]
    )


    df["available_date"] = pd.to_datetime(
        df["available_date"]
    )


    print(
        "股票池:",
        len(df)
    )


    return df





# ============================================================
# 加载交易日
# ============================================================

def load_trade_dates():


    sql = text(
        """
        SELECT DISTINCT

            date


        FROM daily_price_qfq


        WHERE

            date >= :start


        ORDER BY date

        """
    )


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn,
            params={
                "start":START_DATE
            }
        )


    df["date"] = pd.to_datetime(
        df["date"]
    )


    dates = df["date"].tolist()


    print(
        "交易日:",
        len(dates)
    )


    return dates





# ============================================================
# 加载行情缓存
# ============================================================

def load_prices():


    start = time.time()


    print("="*60)

    print(
        "读取行情数据..."
    )


    sql = text(
        """
        SELECT


            date,

            code,

            open,

            close


        FROM daily_price_qfq


        WHERE

            date >= :start


        ORDER BY date

        """
    )



    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn,
            params={
                "start":START_DATE
            }
        )


    print(
        "行情数量:",
        len(df)
    )


    df["date"] = pd.to_datetime(
        df["date"]
    )


    prices = {}



    groups = list(
        df.groupby(
            "date"
        )
    )


    total = len(groups)



    print(
        "开始建立行情缓存..."
    )



    for idx,(date,group) in enumerate(groups):


        day = {}



        for row in group.itertuples():


            day[row.code] = {


                "open":
                row.open,


                "close":
                row.close

            }



        prices[date] = day



        if idx % 500 == 0:


            print(

                "行情缓存:",

                idx,

                "/",

                total,

                f"({idx/total*100:.1f}%)"

            )



    print(

        "行情缓存完成:",

        len(prices),

        "天"

    )


    print(

        "行情缓存耗时:",

        round(

            time.time()-start,

            2

        ),

        "秒"

    )


    return prices

# ============================================================
# 获取目标股票
# ============================================================

def get_target_stocks(
        pool,
        date
):


    available = pool[

        pool["available_date"]
        <=
        date

    ]


    if len(available)==0:

        return set()



    latest = (

        available["pool_date"]

        .max()

    )



    result = available[

        available["pool_date"]

        ==

        latest

    ]



    return set(

        result["code"]

        .tolist()

    )





# ============================================================
# 卖出
# ============================================================

def execute_sell(
        codes,
        prices,
        date
):


    for code in codes:


        if not portfolio.has_position(
            code
        ):

            continue



        if code not in prices:

            continue



        close = prices[code]["close"]


        if close <= 0:

            continue



        price = broker.sell_price(
            close
        )



        shares = (

            portfolio.positions[code]["shares"]

        )



        amount = (

            shares

            *

            price

        )


        fee = broker.sell_cost(
            amount
        )



        sold = portfolio.sell(

            code,

            price,

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
                price,


                "shares":
                sold

            }

        )






# ============================================================
# 买入
# ============================================================

def execute_buy(
        codes,
        prices,
        date
):


    if len(codes)==0:

        return



    cash = portfolio.cash


    if cash <=0:

        return


    # 根据市场状态控制股票仓位
    position_ratio = risk.get_position_ratio(date)

    available_cash = cash * position_ratio


    cash_each = (

        available_cash

        /

        len(codes)

    )



    for code in codes:



        if code not in prices:

            continue



        open_price = prices[code]["open"]



        if open_price<=0:

            continue



        price = broker.buy_price(
            open_price
        )



        shares = broker.calculate_shares(

            cash_each,

            price

        )



        if shares<=0:

            continue



        amount = (

            shares

            *

            price

        )



        fee = broker.buy_cost(
            amount
        )



        success = portfolio.buy(

            code,

            shares,

            price,

            fee

        )



        if success:


            trades.append(

                {

                    "date":
                    date,


                    "code":
                    code,


                    "action":
                    "BUY",


                    "price":
                    price,


                    "shares":
                    shares

                }

            )






# ============================================================
# 组合当前价格
# ============================================================

def get_close_prices(
        today_prices
):


    result={}


    for code,value in today_prices.items():


        result[code]=value["close"]



    return result

# ============================================================
# 保存结果
# ============================================================

def save_results():


    print("="*60)

    print(
        "保存结果..."
    )



    equity = portfolio.get_history()



    equity.to_csv(

        f"{RESULT_DIR}/equity.csv",

        index=False

    )



    trade_df = pd.DataFrame(
        trades
    )



    if len(trade_df)>0:


        trade_df.to_csv(

            f"{RESULT_DIR}/trades.csv",

            index=False

        )



    final_value = (

        equity.iloc[-1]["total_value"]

        if len(equity)>0

        else INITIAL_CASH

    )



    total_return = (

        final_value

        /

        INITIAL_CASH

        -

        1

    ) * 100



    with open(

        f"{RESULT_DIR}/backtest_summary.txt",

        "w"

    ) as f:


        f.write(

            "多因子回测\n"

        )


        f.write(

            f"初始资金:{INITIAL_CASH}\n"

        )


        f.write(

            f"最终资产:{final_value:.2f}\n"

        )


        f.write(

            f"收益率:{total_return:.2f}%\n"

        )


        f.write(

            f"交易次数:{len(trades)}\n"

        )



    print(

        "最终资产:",

        round(
            final_value,
            2
        )

    )


    print(

        "交易次数:",

        len(trades)

    )





# ============================================================
# 主回测
# ============================================================

def run():


    start=time.time()


    print()

    print("="*60)

    print(
        "开始回测"
    )

    print("="*60)



    pool = load_stock_pool()



    dates = load_trade_dates()



    prices = load_prices()



    total_days=len(dates)



    last_rebalance=None



    for idx,date in enumerate(dates):


        today_prices = prices.get(

            date,

            {}

        )



        # =========================================
        # 进度
        # =========================================


        if idx % 250 == 0:


            print()

            print(

                "回测进度:",

                idx,

                "/",

                total_days,

                f"({idx/total_days*100:.1f}%)",

                "日期:",

                date.strftime("%Y-%m-%d")

            )





        # =========================================
        # 判断是否调仓
        # =========================================


        target = get_target_stocks(

            pool,

            date

        )



        if len(target)>0:


            if target != last_rebalance:



                print()

                print(

                    "调仓:",

                    date.strftime("%Y-%m-%d"),

                    "股票:",

                    len(target)

                )



                current = set(

                    portfolio.positions.keys()

                )



                sell_list = (

                    current

                    -

                    target

                )



                buy_list = (

                    target

                    -

                    current

                )



                execute_sell(

                    sell_list,

                    today_prices,

                    date

                )



                execute_buy(

                    buy_list,

                    today_prices,

                    date

                )



                last_rebalance = target





        # =========================================
        # 每日记录
        # =========================================


        close_prices = get_close_prices(

            today_prices

        )


        portfolio.record(

            date,

            close_prices

        )




    print()

    print("="*60)

    print(

        "回测完成"

    )


    print(

        "耗时:",

        round(

            time.time()-start,

            2

        ),

        "秒"

    )


    save_results()





# ============================================================
# 入口
# ============================================================

if __name__=="__main__":


    run()