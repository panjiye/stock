import pandas as pd
from sqlalchemy import text

from data.query import (
    engine,
    get_stock_list,
    get_stock_daily
)

from analysis.indicator import add_indicator

def indicator_done(code):

    sql = text(
        """
        SELECT 1
        FROM daily_indicator
        WHERE code=:code
        LIMIT 1
        """
    )


    with engine.connect() as conn:

        result = conn.execute(
            sql,
            {
                "code": code
            }
        ).fetchone()


    return result is not None

def save_indicator(df):

    code = df["code"].iloc[0]


    with engine.begin() as conn:

        conn.execute(
            text(
                """
                DELETE FROM daily_indicator
                WHERE code=:code
                """
            ),
            {
                "code": code
            }
        )


    df[
        [
            "date",
            "code",

            "MA5",
            "MA10",
            "MA20",
            "MA60",

            "DIF",
            "DEA",
            "MACD",

            "RSI",

            "K",
            "D",
            "J"
        ]
    ].to_sql(
        "daily_indicator",
        engine,
        if_exists="append",
        index=False
    )



def build_one(code):

    print(
        "计算:",
        code
    )


    df = get_stock_daily(code)


    if len(df)==0:

        return False


    df = add_indicator(df)


    save_indicator(df)


    return True




def main():

    stocks = get_stock_list()


    total = len(stocks)


    print(
        "股票数量:",
        total
    )


    success = 0


    for i,row in stocks.iterrows():

        code = row["code"]
        
        if indicator_done(code):

            print(
                "跳过:",
                code
            )

            continue

        try:

            if build_one(code):

                success += 1


        except Exception as e:

            print(
                code,
                "失败:",
                e
            )


        if (i+1)%100==0:

            print(
                f"{i+1}/{total}",
                "完成",
                success
            )


    print(
        "全部完成:",
        success
    )



if __name__=="__main__":

    main()
