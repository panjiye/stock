"""
风险退出回测 v2

基于历史交易记录模拟风险控制

输入:

results_v4_2/trades.csv

格式:

date,code,action,price,shares


数据库:

daily_price_qfq:

date
code
close


daily_indicator:

date
code
MA60


规则:

1. 单股亏损超过30%
2. 跌破MA60持续20交易日


输出:

results_v4_2/risk_stock_exit_v2.csv

"""


import sqlite3
import pandas as pd



DB = "database/stock.db"



MAX_LOSS = -0.30
MA60_DAYS = 20




def load_data():


    trades = pd.read_csv(
        "results_v4_2/trades.csv",
        dtype={
            "code":str
        }
    )


    conn = sqlite3.connect(DB)


    prices = pd.read_sql(
        """
        select
            code,
            date,
            close
        from daily_price_qfq
        """,
        conn
    )


    indicator = pd.read_sql(
        """
        select
            code,
            date,
            MA60
        from daily_indicator
        """,
        conn
    )


    conn.close()


    prices["code"] = prices["code"].astype(str).str.zfill(6)

    indicator["code"] = (
        indicator["code"]
        .astype(str)
        .str.zfill(6)
    )


    return trades, prices, indicator




def check_exit(
        buy_date,
        code,
        buy_price,
        prices,
        indicator
):


    df = prices[
        (prices.code == code)
        &
        (prices.date >= buy_date)
    ].copy()


    if len(df)==0:
        return None


    df=df.sort_values("date")


    ind = indicator[
        (indicator.code==code)
        &
        (indicator.date>=buy_date)
    ].copy()


    df=df.merge(
        ind,
        on=[
            "code",
            "date"
        ],
        how="left"
    )


    df["return"] = (
        df.close-buy_price
    )/buy_price



    #
    # 规则1
    #
    loss = df[
        df["return"] <= MAX_LOSS
    ]


    if len(loss)>0:

        row=loss.iloc[0]

        return {

            "exit_date":row.date,

            "exit_price":row.close,

            "exit_reason":
            "亏损超过30%"

        }




    #
    # 规则2
    #
    if "MA60" in df.columns:


        df["below_ma60"] = (
            df.close < df.MA60
        )


        df["ma60_count"] = (
            df["below_ma60"]
            .rolling(
                MA60_DAYS
            )
            .sum()
        )


        hit=df[
            df.ma60_count >= MA60_DAYS
        ]


        if len(hit)>0:

            row=hit.iloc[0]


            return {

                "exit_date":row.date,

                "exit_price":row.close,

                "exit_reason":
                "跌破MA60超过20天"

            }


    return None




def run():



    trades,prices,indicator = load_data()


    buys = trades[
        trades.action=="BUY"
    ].copy()


    print(
        "买入交易:",
        len(buys)
    )


    results=[]



    for _,row in buys.iterrows():


        code=row.code


        result=check_exit(

            row.date,

            code,

            row.price,

            prices,

            indicator

        )


        if result:


            results.append({

                "code":code,

                "buy_date":row.date,

                "buy_price":row.price,

                "shares":row.shares,

                **result

            })



    result=pd.DataFrame(results)



    if len(result):

        result["return"] = (
            result.exit_price
            -
            result.buy_price
        ) / result.buy_price


        result["pnl"] = (
            result["return"]
            *
            result.shares
            *
            result.buy_price
        )



    output = (
        "results_v4_2/"
        "risk_stock_exit_v2.csv"
    )


    result.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )


    print()

    print(
        "退出数量:",
        len(result)
    )


    if len(result):

        print()

        print(
            result.exit_reason
            .value_counts()
        )


        print()

        print(
            result[
                [
                    "return",
                    "pnl"
                ]
            ]
            .describe()
        )


    print()

    print(
        "输出:",
        output
    )



if __name__=="__main__":

    run()