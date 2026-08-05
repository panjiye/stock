import pandas as pd
import numpy as np

from data.query import engine
from sqlalchemy import text



# ============================================================
# 参数
# ============================================================


INDEX_CODE = "000905"

START_DATE = "2005-01-01"



# ============================================================
# 读取指数
# ============================================================


def load_index():


    sql=text(
        """
        SELECT

            date,
            close

        FROM daily_price_qfq

        WHERE

            code=:code

        AND

            date>=:start

        ORDER BY date

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn,
            params={
                "code":INDEX_CODE,
                "start":START_DATE
            }
        )


    df["date"]=pd.to_datetime(
        df["date"]
    )


    return df





# ============================================================
# 指标
# ============================================================


def calc_return(df):


    return (

        df.iloc[-1]["close"]

        /

        df.iloc[0]["close"]

        -

        1

    )





def calc_annual(df):


    days=(

        df.iloc[-1]["date"]

        -

        df.iloc[0]["date"]

    ).days



    years=days/365



    total=calc_return(df)



    return (

        (1+total)

        **

        (1/years)

        -

        1

    )





def calc_drawdown(df):


    value=df["close"]


    high=value.cummax()


    dd=(

        value-high

    )/high



    return dd.min()





def calc_sharpe(df):


    r=(

        df["close"]

        .pct_change()

        .dropna()

    )


    return (

        r.mean()

        /

        r.std()

        *

        np.sqrt(252)

    )





# ============================================================
# 策略
# ============================================================


def load_strategy():


    df=pd.read_csv(
        "results/equity.csv"
    )


    df["date"]=pd.to_datetime(
        df["date"]
    )


    return df





# ============================================================
# 主程序
# ============================================================


def main():


    print("="*60)

    print(
        "Benchmark分析"
    )

    print("="*60)



    index=load_index()



    strategy=load_strategy()



    print()

    print(
        "中证500"
    )


    print(
        "周期:",
        index.iloc[0]["date"],
        "-",
        index.iloc[-1]["date"]
    )


    print(
        "累计收益:",
        round(
            calc_return(index)*100,
            2
        ),
        "%"
    )


    print(
        "年化收益:",
        round(
            calc_annual(index)*100,
            2
        ),
        "%"
    )


    print(
        "最大回撤:",
        round(
            calc_drawdown(index)*100,
            2
        ),
        "%"
    )


    print(
        "夏普:",
        round(
            calc_sharpe(index),
            2
        )
    )



    print()

    print(
        "策略"
    )


    start=strategy.iloc[0]["total_value"]

    end=strategy.iloc[-1]["total_value"]


    total=(

        end/start

        -

        1

    )



    print(
        "累计收益:",
        round(
            total*100,
            2
        ),
        "%"
    )



if __name__=="__main__":

    main()