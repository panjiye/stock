from sqlalchemy import text

from analysis.query import engine



def main():

    sql1="""

    CREATE TABLE IF NOT EXISTS technical_factor(

        code TEXT,

        date TEXT,


        close REAL,


        ma20 REAL,

        ma60 REAL,

        ma120 REAL,


        return20 REAL,

        return60 REAL,

        return120 REAL,


        volatility REAL,


        trend_score REAL,


        momentum_score REAL,


        technical_score REAL,


        update_time TEXT


    );

    """


    sql2="""

    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_technical_factor_unique

    ON technical_factor(code,date);

    """


    with engine.begin() as conn:

        conn.execute(
            text(sql1)
        )

        conn.execute(
            text(sql2)
        )


    print(
        "技术因子表创建完成"
    )



if __name__=="__main__":

    main()