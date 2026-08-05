import pandas as pd
import numpy as np
import time

from sqlalchemy import text

from data.query import engine



# ============================================================
# 参数
# ============================================================

INITIAL_CAPITAL = 1000000

# 修改:
# 原 TOP100
# 改为 TOP50
TOP_N = 50


# 回测开始时间
BACKTEST_START = "2005-01-01"


# 最少股票数量
MIN_STOCK_COUNT = 30



# ============================================================
# 读取因子数据
# ============================================================


def load_factor_score():


    print()
    print("=" * 60)
    print("读取 factor_score...")


    start=time.time()


    sql=text(
        """
        SELECT

            code,
            pub_date,
            stat_date,
            final_score

        FROM factor_score

        WHERE

            pub_date IS NOT NULL

        AND

            stat_date >= :start_date


        ORDER BY

            code,
            stat_date

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn,
            params={
                "start_date":
                BACKTEST_START
            }
        )


    print(
        "因子记录:",
        len(df)
    )


    print(
        "耗时:",
        round(time.time()-start,2),
        "秒"
    )


    df["pub_date"]=(
        pd.to_datetime(
            df["pub_date"],
            errors="coerce",
            format="mixed"
        )
    )


    df["stat_date"]=(
        pd.to_datetime(
            df["stat_date"],
            errors="coerce",
            format="mixed"
        )
    )


    return df



# ============================================================
# 读取季度调仓日期
# ============================================================


def get_rebalance_dates(df):


    dates=(

        df["stat_date"]

        .drop_duplicates()

        .sort_values()

        .tolist()

    )


    return dates



# ============================================================
# 根据公告日期筛选股票
# ============================================================


def select_stocks(
        factor,
        rebalance_date
):


    print()

    print(
        "筛选日期:",
        rebalance_date.strftime("%Y-%m-%d")
    )


    available=factor[

        factor["pub_date"]
        <=
        rebalance_date

    ].copy()



    print(
        "可用因子:",
        len(available)
    )



    if len(available)==0:

        return []



    available=(

        available

        .sort_values(
            [
                "code",
                "stat_date"
            ]
        )

        .groupby(
            "code"
        )

        .tail(1)

    )



    stock_count=len(available)


    # 新增:
    # 股票太少不交易

    if stock_count < MIN_STOCK_COUNT:

        print(
            "股票数量不足:",
            stock_count
        )

        return []



    available=(

        available

        .sort_values(
            "final_score",
            ascending=False
        )

    )



    result=(

        available

        .head(TOP_N)

        ["code"]

        .tolist()

    )


    print(
        "选股数量:",
        len(result)
    )


    return result



# ============================================================
# 获取下一交易日
# ============================================================


def get_next_trade_day(date):


    sql=text(
        """
        SELECT

            MIN(date) AS date

        FROM daily_price_qfq

        WHERE

            date > :date

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(

            sql,

            conn,

            params={

                "date":

                date.strftime("%Y-%m-%d")

            }

        )


    if df.empty:

        return None


    return pd.to_datetime(

        df.iloc[0]["date"]

    )



# ============================================================
# 获取买入价格
# ============================================================


def get_open_price(
        stocks,
        date
):


    if len(stocks)==0:

        return pd.DataFrame()



    placeholders=",".join(

        ["?"]*len(stocks)

    )



    sql=f"""

    SELECT

        code,

        open


    FROM daily_price_qfq


    WHERE

        date=?


    AND

        code IN ({placeholders})


    """



    params=[

        date.strftime("%Y-%m-%d")

    ]


    params.extend(stocks)



    with engine.connect() as conn:

        df=pd.read_sql(

            sql,

            conn,

            params=tuple(params)

        )



    df=df[

        df["open"]>0

    ]


    return df



# ============================================================
# 获取卖出价格
# ============================================================


def get_close_price(
        stocks,
        date
):


    if len(stocks)==0:

        return pd.DataFrame()



    placeholders=",".join(

        ["?"]*len(stocks)

    )


    sql=f"""

    SELECT

        code,

        close


    FROM daily_price_qfq


    WHERE

        date=?


    AND

        code IN ({placeholders})


    """



    params=[

        date.strftime("%Y-%m-%d")

    ]


    params.extend(stocks)



    with engine.connect() as conn:

        df=pd.read_sql(

            sql,

            conn,

            params=tuple(params)

        )


    df=df[

        df["close"]>0

    ]


    return df
# ============================================================
# 回测核心
# ============================================================


def run_backtest(factor):


    rebalance_dates = get_rebalance_dates(
        factor
    )


    print()
    print("=" * 60)
    print(
        "开始季度多因子回测"
    )

    print(
        "调仓季度:",
        len(rebalance_dates)
    )


    cash = INITIAL_CAPITAL


    equity_curve=[]

    trades=[]



    for i, rebalance_date in enumerate(
            rebalance_dates[:-1]
    ):


        print()
        print("-"*60)


        print(
            "调仓:",
            rebalance_date.strftime("%Y-%m-%d")
        )


        buy_date=get_next_trade_day(
            rebalance_date
        )


        if buy_date is None:

            continue



        stocks=select_stocks(
            factor,
            rebalance_date
        )


        if len(stocks)==0:

            print(
                "跳过本季度"
            )

            continue



        print(
            "买入日期:",
            buy_date.strftime("%Y-%m-%d")
        )



        buy_price=get_open_price(
            stocks,
            buy_date
        )


        if len(buy_price)==0:

            print(
                "没有有效买入价格"
            )

            continue



        sell_date=rebalance_dates[i+1]



        sell_price=get_close_price(
            stocks,
            sell_date
        )



        if len(sell_price)==0:

            print(
                "没有有效卖出价格"
            )

            continue



        portfolio = buy_price.merge(

            sell_price,

            on="code",

            suffixes=(

                "_buy",

                "_sell"

            )

        )



        if len(portfolio)==0:

            continue



        portfolio["return"]=(

            portfolio["close"]

            /

            portfolio["open"]

            -

            1

        )



        period_return=(

            portfolio["return"]

            .mean()

        )



        cash = cash * (

            1+

            period_return

        )



        trades.append(

            {

                "buy_date":
                    buy_date.strftime(
                        "%Y-%m-%d"
                    ),

                "sell_date":
                    sell_date.strftime(
                        "%Y-%m-%d"
                    ),

                "stocks":
                    len(portfolio),

                "return":
                    period_return,

                "value":
                    cash

            }

        )



        equity_curve.append(

            {

                "date":
                    sell_date.strftime(
                        "%Y-%m-%d"
                    ),

                "value":
                    cash

            }

        )



        print(
            "成交股票:",
            len(portfolio)
        )


        print(
            "季度收益:",
            round(
                period_return*100,
                2
            ),
            "%"
        )


        print(
            "资产:",
            round(
                cash,
                2
            )
        )



    return (

        pd.DataFrame(equity_curve),

        pd.DataFrame(trades)

    )




# ============================================================
# 性能指标
# ============================================================


def calculate_performance(
        equity
):


    if len(equity)==0:

        return {}



    equity=equity.copy()



    equity["date"]=pd.to_datetime(

        equity["date"]

    )



    equity=equity.sort_values(

        "date"

    )



    values=(

        equity["value"]

        .astype(float)

    )



    initial=INITIAL_CAPITAL


    final=values.iloc[-1]



    total_return=(

        final

        /

        initial

        -

        1

    )



    # 修改:
    # 使用真实日期计算年数

    days=(

        equity["date"].iloc[-1]

        -

        equity["date"].iloc[0]

    ).days



    years=max(

        days/365,

        0.1

    )



    annual_return=(

        (final/initial)

        **

        (1/years)

        -

        1

    )



    max_value=(

        values

        .cummax()

    )



    drawdown=(

        values

        /

        max_value

        -

        1

    )


    max_drawdown=drawdown.min()



    quarterly_return=(

        values

        .pct_change()

        .dropna()

    )



    if len(quarterly_return)>1:


        sharpe=(

            quarterly_return.mean()

            /

            quarterly_return.std()

            *

            np.sqrt(4)

        )

    else:

        sharpe=0



    return {


        "initial_capital":

            initial,


        "final_value":

            float(final),


        "total_return":

            float(total_return),


        "annual_return":

            float(annual_return),


        "max_drawdown":

            float(max_drawdown),


        "sharpe":

            float(sharpe)

    }




# ============================================================
# 主程序
# ============================================================


def main():


    factor=load_factor_score()



    equity,trades=run_backtest(

        factor

    )



    result=calculate_performance(

        equity

    )



    print()

    print("="*60)

    print(
        "回测完成"
    )


    print(result)



    print()

    print(
        "交易次数:",
        len(trades)
    )



    if len(trades)>0:


        print()

        print(
            trades.head()
        )



    equity.to_csv(

        "backtest_equity.csv",

        index=False

    )



    trades.to_csv(

        "backtest_trades.csv",

        index=False

    )




if __name__=="__main__":

    main()