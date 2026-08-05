#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
export_quant_debug_v3.py

最大回撤研究数据导出

目标:
分析 v4.2 策略最大回撤

2015-06-12 ~ 2018-10-18
"""

import os
import pandas as pd
from data.query import engine



RESULT_DIR = "results_v4_2"

OUTPUT_DIR = "debug_export"


START_DATE = "2015-06-12"
END_DATE = "2018-10-18"


def ensure_dir():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


def save_csv(df, filename):

    path=os.path.join(
        OUTPUT_DIR,
        filename
    )

    df.to_csv(
        path,
        index=False,
        encoding="utf-8-sig"
    )

    size=os.path.getsize(path)/1024/1024

    print(
        f"{filename}: {len(df)} rows {size:.2f} MB"
    )



def export_schema(conn):

    path=os.path.join(
        OUTPUT_DIR,
        "schema.txt"
    )

    tables=conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    ).fetchall()


    with open(
        path,
        "w",
        encoding="utf-8"
    ) as f:

        for t in tables:

            name=t[0]

            f.write(
                "\n\n"
            )

            f.write(
                "="*60
            )

            f.write(
                "\n"
            )

            f.write(
                name
            )

            f.write(
                "\n"
            )


            sql=conn.execute(
                """
                SELECT sql
                FROM sqlite_master
                WHERE name=?
                """,
                (name,)
            ).fetchone()


            if sql:
                f.write(
                    sql[0]
                )



def load_trades():

    path=os.path.join(
        RESULT_DIR,
        "trades.csv"
    )

    return pd.read_csv(path)



def get_codes(df):

    for c in [
        "code",
        "ts_code",
        "symbol"
    ]:

        if c in df.columns:

            return sorted(
                df[c]
                .astype(str)
                .unique()
            )

    return []



def export_trades():

    df=load_trades()

    save_csv(
        df,
        "drawdown_trades.csv"
    )

    return df



def export_equity():

    path=os.path.join(
        RESULT_DIR,
        "equity.csv"
    )

    df=pd.read_csv(path)

    df["date"]=pd.to_datetime(
        df["date"]
    )

    df=df[
        (df.date>=START_DATE)
        &
        (df.date<=END_DATE)
    ]

    save_csv(
        df,
        "drawdown_equity.csv"
    )



def export_price(
        conn,
        codes):


    sql=f"""
    SELECT
        code,
        date,
        close
    FROM daily_price_qfq
    WHERE date>=?
    AND date<=?
    AND code IN
    ({','.join(['?']*len(codes))})
    """


    df=pd.read_sql_query(
        sql,
        conn,
        params=[
            START_DATE,
            END_DATE
        ]+codes
    )


    save_csv(
        df,
        "drawdown_price.csv"
    )



def get_columns(conn,table):

    rows=conn.execute(
        f"PRAGMA table_info({table})"
    ).fetchall()

    return [
        r[1]
        for r in rows
    ]



def export_auto_table(
        conn,
        table,
        filename,
        codes):


    cols=get_columns(
        conn,
        table
    )


    if "code" not in cols:

        print(
            table,
            "skip no code"
        )

        return



    date_col=None


    for c in [
        "date",
        "stat_date",
        "end_date",
        "ann_date",
        "pub_date"
    ]:

        if c in cols:

            date_col=c
            break



    if date_col:


        sql=f"""
        SELECT *
        FROM {table}
        WHERE
        {date_col}>=?
        AND
        {date_col}<=?
        AND
        code IN
        ({','.join(['?']*len(codes))})
        """


        params=[
            START_DATE,
            END_DATE
        ]+codes


    else:


        sql=f"""
        SELECT *
        FROM {table}
        WHERE
        code IN
        ({','.join(['?']*len(codes))})
        """

        params=codes



    df=pd.read_sql_query(
        sql,
        conn,
        params=params
    )


    save_csv(
        df,
        filename
    )



def export_technical(
        conn,
        codes):


    sql=f"""

    SELECT

    code,
    date,

    close,

    ma20,
    ma60,
    ma120,

    return20,
    return60,
    return120,

    volatility,

    trend_score,
    momentum_score,
    technical_score

    FROM technical_factor

    WHERE
    date>=?
    AND
    date<=?

    AND
    code IN
    ({','.join(['?']*len(codes))})

    """


    df=pd.read_sql_query(
        sql,
        conn,
        params=[
            START_DATE,
            END_DATE
        ]+codes
    )


    save_csv(
        df,
        "drawdown_technical_factor.csv"
    )



def main():

    ensure_dir()


    conn=engine.connect(
        DB_PATH
    )


    export_schema(
        conn
    )


    trades=export_trades()


    codes=get_codes(
        trades
    )


    print(
        "stocks:",
        len(codes)
    )


    export_equity()


    export_price(
        conn,
        codes
    )


    export_auto_table(
        conn,
        "stock_industry",
        "drawdown_industry.csv",
        codes
    )


    export_auto_table(
        conn,
        "financial_factor",
        "drawdown_financial_factor.csv",
        codes
    )


    export_auto_table(
        conn,
        "valuation_factor",
        "drawdown_valuation_factor.csv",
        codes
    )


    export_technical(
        conn,
        codes
    )


    conn.close()


    print(
        "DONE"
    )



if __name__=="__main__":

    main()