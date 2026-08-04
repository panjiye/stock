import pandas as pd

from sqlalchemy import text

from analysis.query import engine

from analysis.technical import build_technical



def get_codes():


    sql=text(
        """

        SELECT DISTINCT code

        FROM daily_price_qfq

        ORDER BY code

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    return df["code"].tolist()




def load_one_stock(code):


    sql=text(
        """

        SELECT

            code,

            date,

            close


        FROM daily_price_qfq


        WHERE code=:code


        ORDER BY date


        """

    )


    with engine.connect() as conn:


        df=pd.read_sql(

            sql,

            conn,

            params={
                "code":code
            }

        )


    return df




def save(df):


    df.to_sql(

        "technical_factor",

        engine,

        if_exists="append",

        index=False

    )




def main():


    print(
        "读取股票列表..."
    )


    codes=get_codes()


    print(
        "股票数量:",
        len(codes)
    )


    # 清空旧数据

    with engine.begin() as conn:

        conn.execute(

            text(
                """
                DELETE FROM technical_factor
                """
            )

        )


    count=0


    for code in codes:


        try:


            df=load_one_stock(
                code
            )


            # 数据太少跳过

            if len(df)<120:

                continue



            df["date"]=pd.to_datetime(
                df["date"]
            )


            df=build_technical(
                df
            )


            result=df[

                [

                "code",

                "date",

                "close",

                "ma20",

                "ma60",

                "ma120",

                "return20",

                "return60",

                "return120",

                "volatility",

                "trend_score",

                "momentum_score",

                "technical_score"

                ]

            ]


            save(
                result
            )


            count+=len(result)



            if count%50000==0:

                print(
                    "已处理:",
                    count
                )


        except Exception as e:


            print(
                "错误:",
                code,
                e
            )


    print(
        "完成:",
        count
    )



if __name__=="__main__":

    main()