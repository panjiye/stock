import os
import pandas as pd
import numpy as np
from data.query import engine


RESULT_DIR = "results_v4_2"


# ============================================================
# 数据读取
# ============================================================

def load_equity():

    path = os.path.join(
        RESULT_DIR,
        "equity.csv"
    )

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = df.sort_values(
        "date"
    )

    return df



def load_trades():

    path = os.path.join(
        RESULT_DIR,
        "trades.csv"
    )

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(
        df["date"]
    )

    df = df.sort_values(
        "date"
    )

    return df



def load_price():

    conn = engine.connect(
        DB_PATH
    )

    df = pd.read_sql(
        """
        select
            date,
            code,
            close
        from daily_price_qfq
        """,
        conn
    )

    conn.close()

    df["date"] = pd.to_datetime(
        df["date"]
    )

    return df



# ============================================================
# 最大回撤
# ============================================================

def calculate_drawdown(
    equity
):

    equity["high_water"] = (
        equity["total_value"]
        .cummax()
    )

    equity["drawdown"] = (
        equity["total_value"]
        /
        equity["high_water"]
        -
        1
    )

    return equity



def find_max_drawdown(
    equity
):

    end_idx = (
        equity["drawdown"]
        .idxmin()
    )


    end_date = (
        equity.loc[
            end_idx,
            "date"
        ]
    )


    start_idx = (
        equity.loc[:end_idx,"total_value"]
        .idxmax()
    )


    start_date = (
        equity.loc[
            start_idx,
            "date"
        ]
    )


    return (
        start_date,
        end_date,
        equity.loc[
            end_idx,
            "drawdown"
        ]
    )



# ============================================================
# 交易恢复
# ============================================================

def analyze_trades(
    trades,
    prices,
    start,
    end
):


    period = trades[
        (trades.date >= start)
        &
        (trades.date <= end)
    ].copy()


    print()

    print(
        "回撤期间交易统计"
    )

    print(
        "交易次数:",
        len(period)
    )


    print(
        "买入:",
        len(
            period[
                period.action=="BUY"
            ]
        )
    )


    print(
        "卖出:",
        len(
            period[
                period.action=="SELL"
            ]
        )
    )


    # 当前持仓

    position={}


    for _,row in trades.iterrows():

        code=row.code

        if code not in position:
            position[code]=0


        if row.action=="BUY":

            position[code]+=row.shares


        else:

            position[code]-=row.shares



    # 回撤开始持仓

    holdings={}


    before=trades[
        trades.date<=start
    ]


    for _,row in before.iterrows():

        code=row.code


        if code not in holdings:
            holdings[code]=0


        if row.action=="BUY":

            holdings[code]+=row.shares

        else:

            holdings[code]-=row.shares



    result=[]


    for code,shares in holdings.items():

        if shares<=0:
            continue


        buy=trades[
            (trades.code==code)
            &
            (trades.action=="BUY")
            &
            (trades.date<=start)
        ]


        if len(buy)==0:
            continue


        avg_cost=(
            (buy.price*buy.shares).sum()
            /
            buy.shares.sum()
        )


        sell=trades[
            (trades.code==code)
            &
            (trades.action=="SELL")
            &
            (trades.date>=start)
            &
            (trades.date<=end)
        ]


        if len(sell)>0:

            sell_price=(
                (sell.price*sell.shares).sum()
                /
                sell.shares.sum()
            )

            ret=(
                sell_price
                /
                avg_cost
                -
                1
            )

            status="已卖出"


        else:

            p=prices[
                (prices.code==code)
                &
                (prices.date<=end)
            ].sort_values(
                "date"
            )


            if len(p)>0:

                last=p.close.iloc[-1]

                ret=(
                    last
                    /
                    avg_cost
                    -
                    1
                )

            else:

                ret=np.nan


            status="仍持有"


        result.append(
            {

                "code":code,

                "shares":shares,

                "cost":avg_cost,

                "return":ret,

                "status":status

            }
        )


    df=pd.DataFrame(result)


    if len(df):

        df=df.sort_values(
            "return"
        )


    return df



# ============================================================
# 主程序
# ============================================================

def main():

    print("="*70)
    print("最大回撤归因分析 v2")
    print("="*70)


    equity=load_equity()

    equity=calculate_drawdown(
        equity
    )


    start,end,dd=find_max_drawdown(
        equity
    )


    print()

    print(
        "最大回撤:"
    )

    print(
        "开始:",
        start
    )

    print(
        "结束:",
        end
    )

    print(
        "幅度:",
        f"{dd:.2%}"
    )


    trades=load_trades()

    prices=load_price()


    stocks=analyze_trades(
        trades,
        prices,
        start,
        end
    )


    print()

    print(
        "最大亏损股票 TOP20"
    )

    print(
        stocks.head(20)
        .to_string(
            index=False
        )
    )


    txt=os.path.join(
        RESULT_DIR,
        "drawdown_analysis_v2.txt"
    )


    csv=os.path.join(
        RESULT_DIR,
        "drawdown_stocks.csv"
    )


    stocks.to_csv(
        csv,
        index=False,
        encoding="utf-8-sig"
    )


    with open(
        txt,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "最大回撤分析\n\n"
        )

        f.write(
            f"开始:{start}\n"
        )

        f.write(
            f"结束:{end}\n"
        )

        f.write(
            f"回撤:{dd:.2%}\n\n"
        )

        f.write(
            stocks.head(50)
            .to_string(
                index=False
            )
        )


    print()

    print(
        "生成完成"
    )

    print(
        txt
    )

    print(
        csv
    )



if __name__=="__main__":

    main()