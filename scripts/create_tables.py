import sqlite3
db = "database/stock.db"


def create_tables():

    conn = sqlite3.connect(db)

    cursor = conn.cursor()


    # ======================
    # 原始行情
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_price_raw (

        date TEXT,

        open REAL,

        high REAL,

        low REAL,

        close REAL,

        volume INTEGER,

        amount REAL,

        code TEXT

    )
    """)


    # ======================
    # 前复权行情
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_price_qfq (

        date TEXT,

        open REAL,

        high REAL,

        low REAL,

        close REAL,

        volume INTEGER,

        amount REAL,

        code TEXT

    )
    """)


    # ======================
    # 后复权行情
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_price_hfq (

        date TEXT,

        open REAL,

        high REAL,

        low REAL,

        close REAL,

        volume INTEGER,

        amount REAL,

        code TEXT

    )
    """)


    # ======================
    # 下载日志
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS download_log (

        code TEXT PRIMARY KEY,

        status TEXT,

        message TEXT,

        update_time TEXT

    )
    """)


    # ======================
    # 财务利润数据
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_profit (

        code TEXT,

        pub_date TEXT,

        stat_date TEXT,


        roe_avg REAL,

        np_margin REAL,

        gp_margin REAL,


        net_profit REAL,

        eps_ttm REAL,

        main_business_revenue REAL,


        total_share REAL,

        liqa_share REAL

    )
    """)


    # ======================
    # 财务因子
    # ======================

    cursor.execute("""
    CREATE TABLE financial_factor (

        code TEXT,

        stat_date TEXT,


        roe_score REAL,

        roe_clip REAL,


        net_margin REAL,

        gross_margin REAL,


        eps REAL,


        profit_growth REAL,

        revenue_growth REAL,


        growth_quality REAL,


        stability_score REAL,


        quality_score REAL,


        update_time TEXT

    )""")

    cursor.execute("""
    CREATE UNIQUE INDEX idx_financial_factor_unique
    ON financial_factor(code, stat_date);
    """)
    # ======================
    # 财务因子排名
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_rank (

        code TEXT,

        stat_date TEXT,


        quality_score REAL,

        quality_rank INTEGER,


        roe_rank INTEGER,

        growth_rank INTEGER,


        update_time TEXT

    )
    """)



    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_financial_rank_unique
    ON financial_rank(code, stat_date)
    """)
    # ======================
    # 标准化财务利润数据
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS financial_profit_normalized (

        code TEXT,

        stat_date TEXT,


        roe REAL,

        net_margin REAL,

        gross_margin REAL,


        net_profit REAL,

        eps REAL,

        revenue REAL,


        update_time TEXT

    )
    """)


    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_financial_profit_normalized_unique
    ON financial_profit_normalized(code, stat_date)
    """)
    # ======================
    # 分红数据
    # ======================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dividend (

        code TEXT,

        regist_date TEXT,

        declare_date TEXT,

        pay_date TEXT,

        ex_date TEXT,


        cash_before_tax REAL,

        cash_after_tax REAL,


        bonus_share REAL,

        transfer_share REAL,


        dividend_info TEXT

    )
    """)


    cursor.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS idx_dividend_unique

    ON dividend(code, ex_date)

    """)


    conn.commit()

    conn.close()


    print("数据库表创建完成")





if __name__ == "__main__":
    create_tables()