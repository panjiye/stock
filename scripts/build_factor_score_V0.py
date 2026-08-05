import pandas as pd

from sqlalchemy import text

from data.query import engine



def load_factor_data():

    sql=text(
        """

        SELECT

            f.code,
            f.stat_date,

            f.quality_score,

            v.valuation_score

        FROM financial_factor f


        LEFT JOIN valuation_factor v

        ON

            f.code=v.code

        AND

            f.stat_date=v.stat_date


        """

    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    return df



def load_technical():

    sql=text(
        """

        SELECT

            code,

            date,

            technical_score


        FROM technical_factor


        """

    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    return df



def merge_factor():


    financial=load_factor_data()


    technical=load_technical()


    financial["stat_date"]=pd.to_datetime(
        financial["stat_date"]
    )


    technical["date"]=pd.to_datetime(
        technical["date"]
    )


    # 财务日期匹配最近交易日技术数据

    result=[]


    for code,group in financial.groupby("code"):


        tech=technical[
            technical.code==code
        ].sort_values(
            "date"
        )


        if len(tech)==0:
            continue


        tmp=pd.merge_asof(

            group.sort_values("stat_date"),

            tech[[

                "date",
                "technical_score"

            ]],

            left_on="stat_date",

            right_on="date",

            direction="backward"

        )


        result.append(tmp)


    df=pd.concat(
        result,
        ignore_index=True
    )


    return df



def calculate_score(df):


    df=df.copy()


    df["quality_score"]=(
        df["quality_score"]
        .fillna(0)
    )


    df["valuation_score"]=(
        df["valuation_score"]
        .fillna(0)
    )


    df["technical_score"]=(
        df["technical_score"]
        .fillna(0)
    )


    df["value_score"]=(

        df["valuation_score"]

    )


    df["final_score"]=(

        df["quality_score"]*0.5

        +

        df["valuation_score"]*0.25

        +

        df["technical_score"]*0.25

    )


    return df[

        [

            "code",

            "stat_date",

            "quality_score",

            "valuation_score",

            "technical_score",

            "value_score",

            "final_score"

        ]

    ]



def save(df):


    with engine.begin() as conn:

        conn.execute(

            text(
                """
                DELETE FROM factor_score
                """
            )

        )


    df.to_sql(

        "factor_score",

        engine,

        if_exists="append",

        index=False

    )



def main():

    print(
        "读取因子..."
    )


    df=merge_factor()


    print(
        "合并:",
        len(df)
    )


    score=calculate_score(
        df
    )


    print(
        "生成评分:",
        len(score)
    )


    save(score)


    print(
        "完成"
    )



if __name__=="__main__":

    main()