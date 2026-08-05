from sqlalchemy import text

from data.query import engine



def main():

    sql1="""

    CREATE TABLE IF NOT EXISTS technical_rank(

        code TEXT,

        date TEXT,


        technical_score REAL,


        technical_rank INTEGER,


        update_time TEXT

    );

    """


    sql2="""

    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_technical_rank_unique

    ON technical_rank(code,date);

    """


    with engine.begin() as conn:

        conn.execute(
            text(sql1)
        )

        conn.execute(
            text(sql2)
        )


    print(
        "技术排名表创建完成"
    )



if __name__=="__main__":

    main()