import pandas as pd
import time

from sqlalchemy import text

from analysis.query import engine



# ============================================================
# 参数
# ============================================================

TOP_N = 100



# ============================================================
# 读取因子
# ============================================================


def load_factor():


    print("=" * 60)
    print("读取综合因子...")


    sql = text(
        """
        SELECT

            code,
            pub_date,
            stat_date,
            final_score

        FROM factor_score

        WHERE

            pub_date IS NOT NULL

        ORDER BY

            code,
            stat_date

        """
    )


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn
        )


    print(
        "综合因子:",
        len(df)
    )


    df["pub_date"] = pd.to_datetime(
        df["pub_date"],
        errors="coerce"
    )


    df["stat_date"] = pd.to_datetime(
        df["stat_date"],
        errors="coerce"
    )


    return df




# ============================================================
# 股票基础信息
# ============================================================


def load_basic():


    print("=" * 60)
    print("读取股票信息...")


    sql = text(
        """
        SELECT

            code,
            name,
            ipo_date,
            out_date

        FROM stock_basic

        """
    )


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn
        )


    print(
        "股票数量:",
        len(df)
    )


    df["ipo_date"] = pd.to_datetime(
        df["ipo_date"],
        errors="coerce"
    )


    df["out_date"] = pd.to_datetime(
        df["out_date"],
        errors="coerce"
    )


    return df




# ============================================================
# 生成季度调仓股票池
# ============================================================


def build_pool(factor):


    print("=" * 60)
    print("生成季度股票池...")


    # 使用财报日期作为季度节点

    dates = sorted(
        factor["stat_date"]
        .drop_duplicates()
        .tolist()
    )


    print(
        "季度数量:",
        len(dates)
    )


    result=[]


    for i, rebalance_date in enumerate(dates):


        print(
            "处理:",
            rebalance_date.strftime("%Y-%m-%d")
        )



        # ==========================================
        # 关键:
        # 只能使用已经公告的数据
        # ==========================================


        available = factor[
            factor["pub_date"]
            <=
            rebalance_date
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



        result.append(
            available[
                [
                    "code",
                    "stat_date",
                    "reason"
                ]
            ]
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


    print("=" * 60)
    print("基础过滤...")


    df = pool.merge(
        basic,
        on="code",
        how="left"
    )


    print(
        "合并:",
        len(df)
    )


    before=len(df)



    # -----------------------
    # ST过滤
    # -----------------------


    df=df[
        ~df["name"]
        .fillna("")
        .str.contains(
            "ST"
        )
    ]



    # -----------------------
    # 退市过滤
    # -----------------------


    df=df[
        df["out_date"].isna()
        |
        (
            df["out_date"]
            >
            df["stat_date"]
        )
    ]



    # -----------------------
    # 上市一年过滤
    # -----------------------


    df=df[
        df["ipo_date"].isna()
        |
        (
            df["stat_date"]
            >=
            (
                df["ipo_date"]
                +
                pd.DateOffset(
                    years=1
                )
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
# 保存
# ============================================================


def save(df):


    print("="*50)
    print("写入股票池...")


    result=df[

        [
            "code",
            "stat_date",
            "reason"

        ]

    ].copy()


    # ============================
    # 去除股票池重复记录
    # 一个季度一只股票只能出现一次
    # ============================

    result = (
        result
        .drop_duplicates(
            [
                "code",
                "stat_date"
            ]
        )
    )


    result["enable"]=1


    result["update_time"]=pd.Timestamp.now()



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


    print()
    print("开始生成股票池")
    print()



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



    print("=" * 60)

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