import pandas as pd
import time

from sqlalchemy import text

from data.query import engine



# ============================================================
# 参数
# ============================================================

TOP_N = 100

MIN_AVG_AMOUNT = 50000000

REBALANCE_DAYS = 30



# ============================================================
# 读取因子
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

        WHERE pub_date IS NOT NULL

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    print(
        "因子数量:",
        len(df)
    )


    df["code"]=(
        df["code"]
        .astype(str)
        .str.zfill(6)
    )


    df["pub_date"]=pd.to_datetime(
        df["pub_date"],
        errors="coerce"
    )


    df["stat_date"]=pd.to_datetime(
        df["stat_date"],
        errors="coerce"
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
            out_date

        FROM stock_basic

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    df["code"]=(
        df["code"]
        .astype(str)
        .str.zfill(6)
    )


    return df





# ============================================================
# 交易日
# ============================================================


def load_trade_dates():

    print("="*60)
    print("读取交易日...")


    sql=text(
        """
        SELECT DISTINCT date

        FROM daily_price_qfq

        ORDER BY date

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn
        )


    dates=pd.to_datetime(
        df["date"]
    )


    print(
        "交易日:",
        len(dates)
    )


    return dates





# ============================================================
# 找交易日
# ============================================================


def get_trade_day_after(
        date,
        trade_dates
):


    result=trade_dates[
        trade_dates > date
    ]


    if len(result)==0:

        return None


    return result.iloc[0]





# ============================================================
# 计算调仓日期
# ============================================================


def get_rebalance_date(
        stat_date,
        trade_dates
):


    target = (
        stat_date
        +
        pd.Timedelta(
            days=REBALANCE_DAYS
        )
    )


    return get_trade_day_after(
        target,
        trade_dates
    )





# ============================================================
# 流动性
# ============================================================


def load_liquidity(
        codes
):


    placeholders=",".join(
        ["?"]*len(codes)
    )


    sql=f"""

    SELECT

        code,

        AVG(amount) avg_amount


    FROM

    (

        SELECT

            code,

            amount,

            ROW_NUMBER() OVER(

                PARTITION BY code

                ORDER BY date DESC

            ) rn


        FROM daily_price_qfq


        WHERE code IN ({placeholders})

    )


    WHERE rn<=20


    GROUP BY code

    """



    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn,
            params=tuple(codes)
        )


    return df





# ============================================================
# 生成股票池
# ============================================================


def build_pool(
        factor,
        basic,
        trade_dates
):


    print("="*60)
    print("生成季度股票池...")


    quarters=(

        factor["stat_date"]

        .drop_duplicates()

        .sort_values()

        .tolist()

    )


    print(
        "季度数量:",
        len(quarters)
    )


    result=[]


    for i,stat_date in enumerate(quarters):


        rebalance_date=get_rebalance_date(
            stat_date,
            trade_dates
        )


        if rebalance_date is None:

            continue



        available=factor[

            factor["pub_date"]

            <=

            rebalance_date

        ].copy()



        if len(available)==0:

            continue



        # 每只股票取最新可用财报

        available=(

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


        available["score"]=(
            available["final_score"]
        )



        available["rebalance_date"]=(
            rebalance_date
        )


        available["available_date"]=(
            get_trade_day_after(
                rebalance_date,
                trade_dates
            )
        )



        available=available.merge(
            basic,
            on="code",
            how="left"
        )



        # ST过滤

        available=available[

            ~available["name"]
            .fillna("")
            .str.contains(
                "ST"
            )

        ]



        # 退市过滤

        available["out_date"]=pd.to_datetime(
            available["out_date"],
            errors="coerce"
        )


        available=available[

            available["out_date"].isna()

            |

            (
                available["out_date"]
                >
                available["available_date"]
            )

        ]



        # 上市一年

        available["ipo_date"]=pd.to_datetime(
            available["ipo_date"],
            errors="coerce"
        )


        available=available[

            available["available_date"]

            >=

            (
                available["ipo_date"]

                +

                pd.DateOffset(
                    years=1
                )

            )

        ]



        available=(

            available

            .sort_values(
                "score",
                ascending=False
            )

            .head(
                TOP_N
            )

        )


        available["reason"]="季度因子TOP100"


        result.append(

            available[

                [
                    "code",
                    "stat_date",
                    "pub_date",
                    "rebalance_date",
                    "available_date",
                    "score",
                    "reason"

                ]

            ]

        )



        if i%20==0:

            print(
                "处理:",
                stat_date.strftime("%Y-%m-%d"),
                "股票:",
                len(available)
            )



    pool=pd.concat(
        result,
        ignore_index=True
    )


    print(
        "股票池:",
        len(pool)
    )



    # 流动性

    liquidity=load_liquidity(
        pool["code"]
        .unique()
        .tolist()
    )


    pool=pool.merge(
        liquidity,
        on="code",
        how="left"
    )


    before=len(pool)


    pool=pool[
        pool["avg_amount"]
        >=
        MIN_AVG_AMOUNT
    ]


    print(
        "流动性:",
        before,
        "->",
        len(pool)
    )


    return pool





# ============================================================
# 保存
# ============================================================


def save(pool):


    print("="*60)
    print("保存股票池...")


    pool["enable"]=1

    pool["update_time"]=pd.Timestamp.now()



    pool=pool.drop_duplicates(
        [
            "code",
            "stat_date"
        ]
    )


    pool=pool[

        [
            "code",
            "stat_date",
            "pub_date",
            "rebalance_date",
            "available_date",
            "score",
            "reason",
            "enable",
            "update_time"
        ]

    ]



    with engine.begin() as conn:

        conn.execute(
            text(
                """
                DELETE FROM stock_pool
                """
            )
        )


    pool.to_sql(
        "stock_pool",
        engine,
        if_exists="append",
        index=False
    )


    print(
        "写入:",
        len(pool)
    )





# ============================================================
# 主程序
# ============================================================


def main():

    start=time.time()


    print("\n开始生成股票池\n")


    factor=load_factor()

    basic=load_basic()

    trade_dates=load_trade_dates()


    pool=build_pool(
        factor,
        basic,
        trade_dates
    )


    save(pool)



    print("="*60)

    print("完成")


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