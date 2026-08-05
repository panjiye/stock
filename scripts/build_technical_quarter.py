import pandas as pd

from sqlalchemy import text

from data.query import engine



def main():


    print(
        "开始生成季度技术因子..."
    )


    sql=text(
        """

        SELECT

            code,

            date,

            technical_score


        FROM technical_factor


        ORDER BY

            code,

            date


        """
    )


    print(
        "读取日线技术数据..."
    )


    chunks=[]

    total=0


    with engine.connect() as conn:


        for i,chunk in enumerate(
            pd.read_sql(
                sql,
                conn,
                chunksize=500000
            )
        ):


            chunks.append(chunk)


            total += len(chunk)


            print(
                f"读取第 {i+1} 批, "
                f"累计 {total} 条"
            )



    print(
        "合并数据..."
    )


    df=pd.concat(
        chunks,
        ignore_index=True
    )


    print(
        "技术记录:",
        len(df)
    )



    print(
        "转换日期..."
    )


    df["date"]=pd.to_datetime(
        df["date"]
    )



    print(
        "计算季度..."
    )


    df["quarter"]=(
        df["date"]
        .dt
        .to_period("Q")
    )



    print(
        "提取季度最后交易日..."
    )


    result=(

        df
        .sort_values(
            [
                "code",
                "date"
            ]
        )
        .groupby(
            [
                "code",
                "quarter"
            ],
            sort=False
        )
        .tail(1)

    )


    print(
        "季度记录:",
        len(result)
    )



    print(
        "生成财报日期..."
    )


    result["stat_date"]=(

        result["quarter"]
        .dt
        .to_timestamp(
            "Q"
        )

    )



    result=result[

        [
            "code",

            "stat_date",

            "technical_score"

        ]

    ]



    print(
        "删除旧季度技术表..."
    )


    with engine.begin() as conn:


        conn.execute(

            text(
                """
                DROP TABLE IF EXISTS technical_quarter_factor
                """
            )

        )



    print(
        "写入季度技术数据..."
    )


    result.to_sql(

        "technical_quarter_factor",

        engine,

        index=False

    )


    print(
        "季度技术因子生成完成"
    )



if __name__=="__main__":

    main()