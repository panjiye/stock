import pandas as pd
import numpy as np

from sqlalchemy import text

from data.query import engine



def load_factor():

    sql=text(
        """
        SELECT

            code,

            stat_date,

            roe,

            net_margin,

            gross_margin,

            eps,

            profit_growth,

            revenue_growth,

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



def basic_info(df):

    print()
    print("="*50)
    print("基础信息")
    print("="*50)


    print(
        "财务记录:",
        len(df)
    )


    print(
        "股票数量:",
        df["code"].nunique()
    )


    print(
        "日期范围:"
    )


    print(
        df["stat_date"].min(),
        "~",
        df["stat_date"].max()
    )



def missing_check(df):

    print()
    print("="*50)
    print("字段缺失率")
    print("="*50)


    cols=[

        "roe",

        "net_margin",

        "gross_margin",

        "eps",

        "profit_growth",

        "revenue_growth"

    ]


    for c in cols:


        rate=(

            df[c]
            .isna()
            .mean()

        )


        print(
            c,
            f"{rate:.2%}"
        )



def abnormal_check(df):

    print()
    print("="*50)
    print("异常数据")
    print("="*50)



    print(
        "ROE >100%:"
        ,
        (
            df["roe"]>1
        )
        .sum()
    )



    print(
        "ROE < -100%:"
        ,
        (
            df["roe"]<-1
        )
        .sum()
    )



    print(
        "利润增长>1000%:"
        ,
        (
            df["profit_growth"]>10
        )
        .sum()
    )



    print(
        "收入增长>1000%:"
        ,
        (
            df["revenue_growth"]>10
        )
        .sum()
    )



def stock_coverage(df):


    print()
    print("="*50)
    print("股票覆盖")
    print("="*50)


    result=(

        df
        .groupby("code")
        ["stat_date"]
        .count()
        .sort_values()

    )


    print(
        "财报数量最少:"
    )


    print(
        result.head(10)
    )



    print()

    print(
        "财报数量最多:"
    )


    print(
        result.tail(10)
    )



def continuity_check(df):

    print()
    print("="*50)
    print("连续性检查")
    print("="*50)


    tmp=df.copy()


    tmp["stat_date"]=pd.to_datetime(
        tmp["stat_date"]
    )


    tmp=tmp.sort_values(
        [
            "code",
            "stat_date"
        ]
    )


    tmp["days"]=(
        tmp
        .groupby("code")
        ["stat_date"]
        .diff()
        .dt.days
    )


    print(
        "超过400天间隔:"
    )


    print(

        tmp[
            tmp["days"]>400
        ]
        [
            [
                "code",
                "stat_date",
                "days"
            ]
        ]
        .head(20)

    )



def main():


    print(
        "读取 financial_factor..."
    )


    df=load_factor()



    basic_info(df)


    missing_check(df)


    abnormal_check(df)


    stock_coverage(df)


    continuity_check(df)



if __name__=="__main__":

    main()