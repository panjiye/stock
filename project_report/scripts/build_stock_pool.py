import pandas as pd
import time

from sqlalchemy import text

from analysis.query import engine



# ============================================================
# 参数
# ============================================================

TOP_N = 100



# ============================================================
# 读取综合因子
# ============================================================


def load_factor():

    print("="*60)
    print("读取综合因子...")


    sql=text(
        """
        SELECT

            code,
            pub_date,
            stat_date,
            final_score

        FROM factor_score

        WHERE

            pub_date IS NOT NULL

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    print(
        "综合因子:",
        len(df)
    )


    df["pub_date"]=pd.to_datetime(
        df["pub_date"],
        errors="coerce",
        format="mixed"
    )


    df["stat_date"]=pd.to_datetime(
        df["stat_date"],
        errors="coerce",
        format="mixed"
    )


    return df





# ============================================================
# 股票基本信息
# ============================================================


def load_basic():

    print("="*60)
    print("读取股票信息...")


    sql=text(
        """
        SELECT

            code,
            name,
            ipo_date,
            out_date,
            status

        FROM stock_basic

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    print(
        "股票数量:",
        len(df)
    )


    return df
# ============================================================
# 按公告日期生成季度股票池
# ============================================================


def build_pool(df):


    print("="*60)
    print("生成季度股票池...")


    dates = (
        df["stat_date"]
        .drop_duplicates()
        .sort_values()
        .tolist()
    )


    print(
        "调仓季度:",
        len(dates)
    )


    result=[]


    for i,date in enumerate(dates):


        # ====================================
        # 关键:
        # 只使用当时已经公告的财报
        # ====================================

        available = df[
            df["pub_date"]
            <=
            date
        ].copy()



        if len(available)==0:

            continue



        # 每只股票取最新财报


        available = (
            available
            .sort_values(
                [
                    "code",
                    "stat_date"
                ]
            )
            .groupby(
                "code"
            )
            .tail(1)
        )



        available = (
            available
            .sort_values(
                "final_score",
                ascending=False
            )
            .head(
                TOP_N
            )
        )



        available["reason"] = (
            "公告可用因子TOP100"
        )


        available["pool_date"] = (
            date
        )


        result.append(
            available
        )



        if i % 20 == 0:

            print(
                "处理:",
                date.strftime("%Y-%m-%d"),
                "股票:",
                len(available)
            )



    if len(result)==0:

        return pd.DataFrame()



    pool = pd.concat(
        result,
        ignore_index=True
    )


    print(
        "股票池数量:",
        len(pool)
    )


    return pool





# ============================================================
# 基础过滤
# ============================================================


def filter_basic(pool,basic):


    print("="*60)
    print("基础过滤...")


    df = pool.merge(

        basic,

        on="code",

        how="left"

    )


    before=len(df)


    # -------------------------
    # ST过滤
    # -------------------------


    df=df[
        ~df["name"]
        .fillna("")
        .str.contains(
            "ST"
        )
    ]



    # -------------------------
    # 退市过滤
    # -------------------------


    df["out_date"]=pd.to_datetime(
        df["out_date"],
        errors="coerce"
    )


    df=df[
        df["out_date"].isna()
        |
        (
            df["out_date"]
            >
            df["pool_date"]
        )
    ]



    # -------------------------
    # 上市一年过滤
    # -------------------------


    df["ipo_date"]=pd.to_datetime(
        df["ipo_date"],
        errors="coerce"
    )


    df=df[
        df["pool_date"]
        >=
        (
            df["ipo_date"]
            +
            pd.DateOffset(
                years=1
            )
        )
    ]



    print(
        "过滤:",
        before,
        "->",
        len(df)
    )


    return df





# ============================================================
# 保存股票池
# ============================================================


def save(df):


    print("="*60)
    print("写入股票池...")



    result=df[

        [
            "code",
            "pool_date",
            "pub_date",
            "reason"

        ]

    ].copy()



    result.rename(

        columns={

            "pool_date":
            "stat_date"

        },

        inplace=True

    )



    result["enable"]=1


    result["update_time"]=pd.Timestamp.now()



    # 去重

    result=result.drop_duplicates(

        subset=[

            "code",
            "stat_date"

        ]

    )



    with engine.begin() as conn:

        conn.execute(

            text(
                """
                DELETE FROM stock_pool
                """
            )

        )



    result.to_sql(

        "stock_pool",

        engine,

        if_exists="append",

        index=False

    )


    print(
        "写入:",
        len(result)
    )

# ============================================================
# 主程序
# ============================================================


def main():


    start=time.time()


    print(
        "\n开始生成股票池\n"
    )



    factor=load_factor()


    basic=load_basic()



    pool=build_pool(
        factor
    )



    pool=filter_basic(
        pool,
        basic
    )



    save(
        pool
    )



    print("="*60)

    print(
        "完成"
    )


    print(
        "耗时:",
        round(
            time.time()-start,
            2
        ),
        "秒"
    )




if __name__=="__main__":

    main()