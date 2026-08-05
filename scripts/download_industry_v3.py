"""
下载A股行业分类

数据源:
东方财富行业分类

写入:
stock_industry

"""

import datetime
import sqlite3

import akshare as ak

from data.query import DB_PATH



def download_industry():

    print("=" * 60)
    print("开始下载股票行业分类")
    print("=" * 60)


    print("获取行业列表...")


    industry_df = ak.stock_board_industry_name_em()


    print(
        f"行业数量: {len(industry_df)}"
    )


    conn = sqlite3.connect(
        DB_PATH
    )

    cur = conn.cursor()


    # 清空旧数据

    cur.execute(
        "DELETE FROM stock_industry"
    )


    total = 0


    today = datetime.date.today().isoformat()


    for _, row in industry_df.iterrows():

        industry = row["板块名称"]

        print(
            f"下载行业: {industry}"
        )


        try:

            stocks = ak.stock_board_industry_cons_em(
                symbol=industry
            )


        except Exception as e:

            print(
                "失败:",
                industry,
                e
            )

            continue



        for _, stock in stocks.iterrows():


            code = str(
                stock["代码"]
            ).zfill(6)


            name = stock["名称"]


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
                    "eastmoney",
                    today
                )
            )


            total += 1



    conn.commit()

    conn.close()


    print("=" * 60)

    print(
        f"写入股票数量: {total}"
    )

    print("=" * 60)



if __name__ == "__main__":

    download_industry()