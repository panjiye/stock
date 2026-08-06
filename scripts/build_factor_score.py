import pandas as pd
import time

from sqlalchemy import text

from data.query import engine
from data.writer import insert_dataframe



def read_table(sql, name):

    print()
    print("=" * 50)
    print(f"读取{name}...")

    start = time.time()

    with engine.connect() as conn:

        df = pd.read_sql(
            text(sql),
            conn
        )


    print(
        f"{name}记录:",
        len(df)
    )

    print(
        f"耗时: {time.time()-start:.2f} 秒"
    )

    return df



def normalize_date(df):

    df["stat_date"] = (
        pd.to_datetime(
            df["stat_date"],
            errors="coerce",
            format="mixed"
        )
        .dt.strftime(
            "%Y-%m-%d"
        )
    )


    if "pub_date" in df.columns:

        df["pub_date"] = (
            pd.to_datetime(
                df["pub_date"],
                errors="coerce",
                format="mixed"
            )
            .dt.strftime(
                "%Y-%m-%d"
            )
        )


    return df


def load_factor():


    financial = read_table(
        """
        SELECT

            code,
            pub_date,
            stat_date,
            quality_score

        FROM financial_factor

        """,
        "财务因子"
    )


    financial = normalize_date(
        financial
    )



    valuation = read_table(
        """
        SELECT

            code,
            pub_date,
            stat_date,
            valuation_score

        FROM valuation_factor

        """,
        "估值因子"
    )


    valuation = normalize_date(
        valuation
    )



    technical = read_table(
        """
        SELECT

            code,
            stat_date,
            technical_score

        FROM technical_quarter_factor

        """,
        "季度技术因子"
    )


    technical = normalize_date(
        technical
    )


    return (
        financial,
        valuation,
        technical
    )



def build_score():


    financial, valuation, technical = load_factor()



    print()
    print("=" * 50)
    print("开始合并财务 + 估值...")


    start=time.time()


    df = financial.merge(

        valuation,

        on=[
            "code",
            "stat_date"
        ],

        how="inner"

    )
    df["pub_date"] = df["pub_date_x"]

    df.drop(
        columns=[
            "pub_date_x",
            "pub_date_y"
        ],
        inplace=True
    )
    print(
        "合并后:",
        len(df)
    )


    print(
        f"耗时:{time.time()-start:.2f} 秒"
    )



    print()
    print("=" * 50)
    print("开始合并季度技术...")


    start=time.time()


    df = df.merge(

        technical,

        on=[
            "code",
            "stat_date"
        ],

        how="left"

    )


    print(
        "合并技术后:",
        len(df)
    )


    print(
        f"耗时:{time.time()-start:.2f} 秒"
    )



    print()

    missing = (
        df["technical_score"]
        .isna()
        .sum()
    )


    print(
        "技术因子缺失:",
        missing
    )


    print(
        "技术因子覆盖:",
        len(df)-missing
    )



    print()
    print("=" * 50)
    print("计算最终评分...")



    df["technical_score"] = (
        df["technical_score"]
        .fillna(0)
    )


    df["quality_score"] = (
        df["quality_score"]
        .fillna(0)
    )


    df["valuation_score"] = (
        df["valuation_score"]
        .fillna(0)
    )



    df["final_score"] = (

        df["quality_score"]
        *
        0.4

        +

        df["valuation_score"]
        *
        0.3

        +

        df["technical_score"]
        *
        0.3

    )



    result = df[

        [
            "code",
            "pub_date",            
            "stat_date",
            "quality_score",
            "valuation_score",
            "technical_score",
            "final_score"
        ]

    ]


    return result



def save(df):


    print()
    print("=" * 50)
    print("写入 factor_score...")


    start=time.time()


    with engine.begin() as conn:

        conn.execute(
            text(
                """
                DELETE FROM factor_score
                """
            )
        )



    insert_dataframe(

        df,

        "factor_score",

        if_exists="append"

    )


    print(
        "写入完成:",
        len(df)
    )


    print(
        f"耗时:{time.time()-start:.2f} 秒"
    )



def main():


    print()
    print("开始生成综合因子...")


    start=time.time()


    df = build_score()


    save(df)


    print()
    print("=" * 50)
    print("全部完成")


    print(
        f"总耗时:{time.time()-start:.2f} 秒"
    )



if __name__=="__main__":

    main()