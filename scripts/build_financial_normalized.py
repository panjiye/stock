import pandas as pd

from sqlalchemy import text


from data.query import engine
from data.writer import insert_dataframe

from analysis.financial_normalize import (
    normalize_financial_profit
)



def load_financial_profit():


    sql=text(
        """
        SELECT

            code,
            pub_date,
            stat_date,

            roe_avg,

            np_margin,

            gp_margin,

            net_profit,

            eps_ttm,

            main_business_revenue


        FROM financial_profit

        ORDER BY
            code,
            stat_date

        """
    )


    with engine.connect() as conn:


        df=pd.read_sql(
            sql,
            conn
        )


    return df



def save_normalized(df):


    with engine.begin() as conn:


        conn.execute(
            text(
                """
                DELETE FROM financial_profit_normalized
                """
            )
        )



    insert_dataframe(
        df,
        "financial_profit_normalized",
        if_exists="append"
    )



def main():


    print(
        "读取 financial_profit..."
    )


    df=load_financial_profit()


    print(
        "原始记录:",
        len(df)
    )


    normalized=normalize_financial_profit(
        df
    )


    print(
        "标准化记录:",
        len(normalized)
    )


    save_normalized(
        normalized
    )


    print(
        "完成"
    )



if __name__=="__main__":

    main()