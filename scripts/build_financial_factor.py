import pandas as pd

from sqlalchemy import text

from data.query import engine

from analysis.financial_factor import (
    calculate_financial_factor
)



def load_normalized_profit():


    sql=text(
        """

        SELECT

            code,
            pub_date,
            stat_date,
            roe,
            net_margin,
            gross_margin,
            net_profit,
            eps,
            revenue


        FROM financial_profit_normalized


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




def save_factor(df):


    with engine.begin() as conn:


        conn.execute(

            text(
                """
                DELETE FROM financial_factor
                """
            )

        )


    df.to_sql(

        "financial_factor",

        engine,

        if_exists="append",

        index=False

    )



def main():


    print(
        "读取标准化财务数据..."
    )


    df=load_normalized_profit()


    print(
        "记录:",
        len(df)
    )


    factor=calculate_financial_factor(
        df
    )


    print(
        "生成因子:",
        len(factor)
    )


    save_factor(
        factor
    )


    print(
        "完成"
    )



if __name__=="__main__":

    main()