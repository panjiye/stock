import pandas as pd
import time

from sqlalchemy import text

from analysis.query import engine



TOP_N = 100

MIN_AVG_AMOUNT = 50000000

REBALANCE_DAYS = 30



# ============================================================
# 因子
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
        df["pub_date"]
    )


    df["stat_date"]=pd.to_datetime(
        df["stat_date"]
    )


    return df





# ============================================================
# 股票信息
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


    return pd.to_datetime(
        df["date"]
    )





def next_trade_day(
        date,
        trade_dates
):

    x=trade_dates[
        trade_dates > date
    ]


    if len(x)==0:

        return None


    return x.iloc[0]





# ============================================================
# 调仓日期
# ============================================================

def calc_rebalance_date(
        pool_date,
        trade_dates
):


    target=(

        pool_date

        +

        pd.Timedelta(
            days=REBALANCE_DAYS
        )

    )


    return next_trade_day(
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


    FROM daily_price_qfq


    WHERE code IN ({placeholders})


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
# 股票池
# ============================================================

def build_pool(
        factor,
        basic,
        trade_dates
):


    print("="*60)
    print("生成季度股票池...")


    pool_dates=(

        factor["stat_date"]

        .drop_duplicates()

        .sort_values()

        .tolist()

    )


    print(
        "季度数量:",
        len(pool_dates)
    )


    result=[]


    for i,pool_date in enumerate(pool_dates):


        rebalance_date=calc_rebalance_date(
            pool_date,
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



        # 每股票取最新可用财报

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


        available["pool_date"]=pool_date


        available["factor_date"]=(
            available["stat_date"]
        )


        available["rebalance_date"]=(
            rebalance_date
        )


        available["available_date"]=(
            next_trade_day(
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
            .str.contains("ST")

        ]



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



        available=available.sort_values(
            "final_score",
            ascending=False
        ).head(
            TOP_N
        )



        available["score"]=(
            available["final_score"]
        )


        available["reason"]="季度因子TOP100"


        result.append(

            available[

            [
            "code",
            "pool_date",
            "factor_date",
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
                pool_date.strftime("%Y-%m-%d"),
                len(available)
            )



    pool=pd.concat(
        result,
        ignore_index=True
    )


    print(
        "初始股票池:",
        len(pool)
    )



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


    pool["enable"]=1

    pool["update_time"]=pd.Timestamp.now()


    pool=pool.drop_duplicates(
        [
            "code",
            "pool_date"
        ]
    )


    pool=pool[
        [
        "code",
        "pool_date",
        "factor_date",
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
# main
# ============================================================

def main():

    start=time.time()


    print(
        "\n开始生成股票池\n"
    )


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
        round(time.time()-start,2),
        "秒"
    )





if __name__=="__main__":

    main()