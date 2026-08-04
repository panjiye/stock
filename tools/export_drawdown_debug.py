import sqlite3
import os
import pandas as pd


DB_PATH = "database/stock.db"

OUT_DIR = "debug_snapshot"


START_DATE = "2015-06-12"
END_DATE = "2018-10-18"


def export_csv(df, filename):
    path = os.path.join(OUT_DIR, filename)
    df.to_csv(path, index=False, encoding="utf-8-sig")
    print("export:", path, len(df))


def main():

    os.makedirs(OUT_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)


    print("\n========== DATABASE TABLES ==========")

    tables = pd.read_sql(
        """
        select name 
        from sqlite_master
        where type='table'
        order by name
        """,
        conn
    )

    export_csv(
        tables,
        "tables.csv"
    )


    print("\n========== TABLE COUNT ==========")

    counts=[]

    for t in tables["name"]:

        try:

            c=pd.read_sql(
                f"select count(*) as cnt from {t}",
                conn
            )

            counts.append(
                {
                    "table":t,
                    "count":c.iloc[0]["cnt"]
                }
            )

        except Exception as e:
            pass


    export_csv(
        pd.DataFrame(counts),
        "table_counts.csv"
    )


    print("\n========== SCHEMA ==========")

    schema=[]

    for t in tables["name"]:

        try:

            rows=conn.execute(
                f"pragma table_info({t})"
            ).fetchall()

            for r in rows:

                schema.append(
                    {
                        "table":t,
                        "column":r[1],
                        "type":r[2]
                    }
                )

        except:
            pass


    export_csv(
        pd.DataFrame(schema),
        "schema.csv"
    )


    print("\n========== RESULTS TRADES ==========")


    trade_file="results_v4_2/trades.csv"

    if os.path.exists(trade_file):

        trades=pd.read_csv(trade_file)

        export_csv(
            trades,
            "trades_v4_2.csv"
        )


        if "code" in trades.columns:

            codes=trades["code"].unique().tolist()

        else:

            codes=[]


    else:

        codes=[]



    print("\n========== STOCK BASIC ==========")

    if codes:

        placeholders=",".join(
            ["?"]*len(codes)
        )

        for table in [
            "stock_basic",
            "stock_industry"
        ]:

            try:

                df=pd.read_sql(
                    f"""
                    select *
                    from {table}
                    where code in ({placeholders})
                    """,
                    conn,
                    params=codes
                )

                export_csv(
                    df,
                    f"{table}_drawdown.csv"
                )

            except Exception as e:

                print(
                    table,
                    e
                )


    print("\n========== FACTOR SNAPSHOT ==========")


    factor_tables=[
        "factor_score",
        "financial_factor",
        "technical_factor",
        "valuation_factor"
    ]


    for table in factor_tables:

        try:

            df=pd.read_sql(
                f"""
                select *
                from {table}
                where date between ?
                and ?
                """,
                conn,
                params=[
                    START_DATE,
                    END_DATE
                ]
            )


            if codes and "code" in df.columns:

                df=df[
                    df["code"].isin(codes)
                ]


            export_csv(
                df,
                f"{table}_drawdown.csv"
            )


        except Exception as e:

            print(
                table,
                "skip",
                e
            )



    print("\n========== DAILY PRICE SAMPLE ==========")


    try:

        if codes:

            placeholders=",".join(
                ["?"]*len(codes)
            )


            df=pd.read_sql(
                f"""
                select *
                from daily_price_qfq
                where code in ({placeholders})
                and date between ?
                and ?
                """,
                conn,
                params=
                codes+
                [
                    START_DATE,
                    END_DATE
                ]
            )


            export_csv(
                df,
                "daily_price_drawdown.csv"
            )


    except Exception as e:

        print(
            "daily_price error:",
            e
        )



    conn.close()


    print("\nDONE")


if __name__=="__main__":
    main()
