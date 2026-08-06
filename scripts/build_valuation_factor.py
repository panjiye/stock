import pandas as pd
import numpy as np

from sqlalchemy import text

from data.query import engine
from data.writer import insert_dataframe



def load_data():

    sql=text(
    """

    SELECT

        f.code,
        f.pub_date,
        f.stat_date,

        f.eps,

        p.close


    FROM financial_profit_normalized f


    LEFT JOIN daily_price_qfq p

    ON

        f.code=p.code

    AND

        p.date=f.stat_date


    ORDER BY

        f.code,

        f.stat_date


    """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    return df




def calculate(df):


    df=df.copy()

    df["pub_date"]=(
        pd.to_datetime(
            df["pub_date"],
            errors="coerce",
            format="mixed"
        )
        .dt.strftime("%Y-%m-%d")
    )


    df["pe"]=(
        df["close"]
        /
        df["eps"]
    )


    df["pe"]=(
        df["pe"]
        .replace(
            [np.inf,-np.inf],
            np.nan
        )
    )


    # 删除异常

    df.loc[
        df.pe<0,
        "pe"
    ]=np.nan


    # PE排名

    df["pe_rank"]=(
        df.groupby(
            "stat_date"
        )["pe"]
        .rank(
            pct=True,
            ascending=False
        )
    )


    # 越低PE越好

    df["valuation_score"]=(
        1-df["pe_rank"]
    )


    return df[
        [
            "code",
            "pub_date",            
            "stat_date",
            "close",
            "eps",
            "pe",
            "pe_rank",
            "valuation_score"
        ]
    ]




def save(df):


    with engine.begin() as conn:

        conn.execute(
            text(
            """
            DELETE FROM valuation_factor
            """
            )
        )


    insert_dataframe(
        df,
        "valuation_factor",
        if_exists="append"
    )




def main():


    print(
        "读取财务和行情..."
    )


    df=load_data()


    print(
        "记录:",
        len(df)
    )


    result=calculate(
        df
    )


    print(
        "生成估值:",
        len(result)
    )


    save(
        result
    )


    print(
        "完成"
    )



if __name__=="__main__":

    main()