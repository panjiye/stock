import sqlite3
import requests
import time


DB_PATH = "database/stock.db"


URL = (
    "https://datacenter-web.eastmoney.com/"
    "api/data/v1/get"
)


REPORT_NAME = "RPT_LICO_FN_CPD"


PAGE_SIZE = 500


HEADERS = {
    "User-Agent":
        "Mozilla/5.0"
}



# ======================
# 数据库
# ======================

def get_conn():

    return sqlite3.connect(DB_PATH)



def init_table():

    conn=get_conn()

    cur=conn.cursor()


    cur.execute("""
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


    cur.execute("""
    CREATE UNIQUE INDEX IF NOT EXISTS
    idx_financial_profit_unique

    ON financial_profit(code,stat_date)
    """)


    conn.commit()

    conn.close()



# ======================
# 已存在数据
# ======================

def load_exists():


    conn=get_conn()

    cur=conn.cursor()


    cur.execute("""
    SELECT code,stat_date
    FROM financial_profit
    """)


    rows=cur.fetchall()


    conn.close()


    return set(rows)



# ======================
# 东方财富批量接口
# ======================

def fetch_page(page):


    params={

        "reportName":
            REPORT_NAME,


        "columns":
            "ALL",


        "pageNumber":
            page,


        "pageSize":
            PAGE_SIZE

    }


    r=requests.get(

        URL,

        params=params,

        headers=HEADERS,

        timeout=20

    )


    return r.json()



# ======================
# 保存
# ======================

def save_rows(rows,exists):


    insert=[]


    for item in rows:


        code=item.get(
            "SECURITY_CODE"
        )


        stat=item.get(
            "REPORTDATE"
        )


        if not code or not stat:

            continue


        stat=stat[:10]


        key=(code,stat)


        if key in exists:

            continue



        insert.append(

            (

            code,

            item.get(
                "NOTICE_DATE"
            ),

            stat,


            item.get(
                "WEIGHTAVG_ROE"
            ),


            None,


            item.get(
                "XSMLL"
            ),


            item.get(
                "PARENT_NETPROFIT"
            ),


            item.get(
                "BASIC_EPS"
            ),


            item.get(
                "TOTAL_OPERATE_INCOME"
            ),


            None,


            None

            )

        )


    if not insert:

        return 0



    conn=get_conn()

    cur=conn.cursor()


    cur.executemany(

        """
        INSERT OR IGNORE INTO financial_profit

        VALUES
        (?,?,?,?,?,?,?,?,?,?,?)

        """,

        insert

    )


    conn.commit()

    conn.close()


    return len(insert)



# ======================
# 主程序
# ======================

def main():


    init_table()


    exists=load_exists()


    print(
        "已有记录:",
        len(exists)
    )


    first=fetch_page(1)


    if not first.get("result"):

        print(first)

        return



    total_pages=first["result"]["pages"]


    print(
        "总页数:",
        total_pages
    )


    total_new=0



    for page in range(
        99,
        total_pages+1
    ):


        print(
            f"下载 {page}/{total_pages}"
        )


        data=fetch_page(page)


        rows=data["result"]["data"]


        n=save_rows(
            rows,
            exists
        )


        total_new+=n


        print(
            "新增:",
            n
        )


        time.sleep(
            0.3
        )



    print()

    print(
        "完成"
    )

    print(
        "新增总数:",
        total_new
    )



if __name__=="__main__":

    main()