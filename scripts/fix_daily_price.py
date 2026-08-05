import sqlite3


db = "database/stock.db"

def fix_daily_price():

    conn = sqlite3.connect(db)

    cursor = conn.cursor()


    # 新表
    cursor.execute("""
    CREATE TABLE daily_price_new (
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


    # 转换数据
    cursor.execute("""
    INSERT INTO daily_price_new
    SELECT
        date,
        CAST(open AS REAL),
        CAST(high AS REAL),
        CAST(low AS REAL),
        CAST(close AS REAL),
        CAST(volume AS INTEGER),
        CAST(amount AS REAL),
        code
    FROM daily_price
    """)


    # 删除旧表
    cursor.execute("""
    DROP TABLE daily_price
    """)


    # 改名
    cursor.execute("""
    ALTER TABLE daily_price_new
    RENAME TO daily_price
    """)


    # 重建索引
    cursor.execute("""
    CREATE INDEX idx_daily_code_date
    ON daily_price(code,date)
    """)


    conn.commit()

    conn.close()

    print("daily_price 类型修正完成")

if __name__ == "__main__":
    fix_daily_price()