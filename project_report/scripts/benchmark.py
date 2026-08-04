import pandas as pd

from sqlalchemy import text

from analysis.query import engine



def main():


    print("="*60)

    print(
        "生成Benchmark"
    )


    sql=text(
        """

        SELECT

            date,

            close


        FROM index_price


        WHERE

            code='000300.SH'


        ORDER BY

            date


        """
    )


    with engine.connect() as conn:


        df=pd.read_sql(
            sql,
            conn
        )


    if len(df)==0:

        print(
            "数据库没有000300指数数据"
        )

        return



    df["date"]=pd.to_datetime(
        df["date"]
    )


    df=df.sort_values(
        "date"
    )


    df["benchmark"]=(
        df["close"]
        /
        df["close"].iloc[0]
    )



    df.to_csv(
        "benchmark.csv",
        index=False
    )


    print(
        "Benchmark完成"
    )


    print(
        df.head()
    )



if __name__=="__main__":

    main()