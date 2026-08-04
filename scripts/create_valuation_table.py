from sqlalchemy import text

from analysis.query import engine



def main():

    sql_table = """

    CREATE TABLE IF NOT EXISTS valuation_factor (

        code TEXT,

        stat_date TEXT,

        close REAL,

        eps REAL,

        pe REAL,

        pe_rank REAL,

        valuation_score REAL,

        update_time TEXT

    );

    """


    sql_index = """

    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_valuation_factor_unique

    ON valuation_factor(code,stat_date);

    """


    with engine.begin() as conn:


        conn.execute(
            text(sql_table)
        )


        conn.execute(
            text(sql_index)
        )


    print(
        "估值表创建完成"
    )



if __name__=="__main__":

    main()