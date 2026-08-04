import sqlite3
from datetime import datetime

import tushare as ts

from config.tushare_config import TUSHARE_TOKEN


DB_PATH = "database/stock.db"


def get_engine():

    return ts.pro_api(
        TUSHARE_TOKEN
    )


def download_industry():

    print("=" * 60)
    print("开始下载股票行业分类(Tushare)")
    print("=" * 60)


    pro = get_engine()


    print("获取股票基础信息...")


    df = pro.stock_basic(
        exchange="",
        list_status="L",
        fields=
        """
        ts_code,
        symbol,
        name,
        industry
        """
    )


    print(
        f"股票数量: {len(df)}"
    )


    conn = sqlite3.connect(
        DB_PATH
    )

    cur = conn.cursor()


    update_date = datetime.now().strftime(
        "%Y-%m-%d"
    )


    count = 0


    for _, row in df.iterrows():

        code = row["symbol"]

        name = row["name"]

        industry = row["industry"]


        if industry is None:
            industry = ""


        cur.execute(
            """
            INSERT OR REPLACE INTO stock_industry
            (
                code,
                name,
                industry,
                source,
                update_date
            )
            VALUES
            (
                ?,
                ?,
                ?,
                ?,
                ?
            )
            """,
            (
                code,
                name,
                industry,
                "tushare",
                update_date
            )
        )

        count += 1



    conn.commit()
    conn.close()


    print()
    print("=" * 60)
    print(
        f"写入完成: {count}"
    )
    print("=" * 60)



if __name__ == "__main__":

    download_industry()