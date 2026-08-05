import pandas as pd
from datetime import datetime

from sqlalchemy import text

from data.query import engine



def load_factor():

    sql=text(
        """
        SELECT

            code,

            stat_date,

            roe,

            profit_growth,

            quality_score


        FROM financial_factor

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    return df


def build_rank(df):


    df=df.copy()


    df["stat_date"]=pd.to_datetime(
        df["stat_date"]
    )


    result=[]


    for date,group in df.groupby(
        "stat_date"
    ):


        group=group.copy()



        # =====================
        # 综合质量排名
        # =====================

        group["quality_rank"]=(
            group["quality_score"]
            .rank(
                ascending=False,
                method="first"
            )
        )



        # =====================
        # ROE排名
        # =====================

        group["roe_rank"]=(
            group["roe"]
            .rank(
                ascending=False,
                method="first"
            )
        )



        # =====================
        # 增长排名
        # =====================

        group["growth_rank"]=(
            group["profit_growth"]
            .rank(
                ascending=False,
                method="first"
            )
        )


        result.append(
            group
        )



    df=pd.concat(
        result
    )



    # =====================
    # 缺失排名处理
    # =====================

    df["quality_rank"]=(
        df["quality_rank"]
        .fillna(999999)
        .astype(int)
    )


    df["roe_rank"]=(
        df["roe_rank"]
        .fillna(999999)
        .astype(int)
    )


    df["growth_rank"]=(
        df["growth_rank"]
        .fillna(999999)
        .astype(int)
    )



    df["update_time"]=datetime.now()



    return df[
        [
            "code",
            "stat_date",
            "quality_score",
            "quality_rank",
            "roe_rank",
            "growth_rank",
            "update_time"
        ]
    ]




def save_rank(df):


    with engine.begin() as conn:


        conn.execute(
            text(
                """
                DELETE FROM financial_rank
                """
            )
        )


    df.to_sql(

        "financial_rank",

        engine,

        if_exists="append",

        index=False

    )





def main():


    print(
        "读取财务因子..."
    )


    df=load_factor()


    print(
        "记录:",
        len(df)
    )


    rank=build_rank(
        df
    )


    print(
        "生成排名:",
        len(rank)
    )


    save_rank(
        rank
    )


    print(
        "完成"
    )



if __name__=="__main__":

    main()