import sqlite3
import time
import os

from download_one_stock import download_stock


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


db = os.path.join(
    BASE_DIR,
    "database",
    "stock.db"
)


conn = sqlite3.connect(db)

cursor = conn.cursor()


# 每次下载数量
LIMIT = 5


cursor.execute(
    """
    SELECT code,name
    FROM stock_basic
    WHERE code NOT IN (
        SELECT code
        FROM download_log
        WHERE status='success'
    )
    LIMIT ?
    """,
    (LIMIT,)
)


stocks = cursor.fetchall()


conn.close()


print(
    f"本次准备下载 {len(stocks)} 只股票"
)


success = 0
failed = 0


for i,(code,name) in enumerate(stocks,1):


    print(
        "=" * 40
    )


    print(
        f"[{i}/{len(stocks)}]",
        code,
        name
    )


    try:

        result = download_stock(code)


        if result:

            success += 1


        else:

            failed += 1


    except Exception as e:


        failed += 1


        print(
            "异常:",
            e
        )


    # 防止请求过快
    time.sleep(0.5)



print(
    "=" * 40
)


print(
    "本次完成"
)


print(
    "成功:",
    success
)


print(
    "失败:",
    failed
)