import sqlite3
import requests
import time


DB_PATH = "database/stock.db"


URL = (
    "https://emweb.securities.eastmoney.com/"
    "PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew"
)


HEADERS = {
    "User-Agent":
        "Mozilla/5.0",
    "Referer":
        "https://emweb.securities.eastmoney.com/"
}


# 测试用
# 全量运行改成 None
TEST_LIMIT = 10



# =========================
# 数据库
# =========================

def conn_db():

    return sqlite3.connect(DB_PATH)



def init_table():

    conn = conn_db()
    cur = conn.cursor()


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

    ON financial_profit(code, stat_date)
    """)


    conn.commit()
    conn.close()



# =========================
# 股票列表
# =========================

def get_stocks():

    conn = conn_db()
    cur = conn.cursor()


    cur.execute("""
    SELECT code
    FROM stock_basic
    ORDER BY code
    """)


    rows = cur.fetchall()

    conn.close()


    return [
        x[0]
        for x in rows
    ]



# =========================
# 已有季度
# =========================

def existing_dates(code):

    conn = conn_db()

    cur = conn.cursor()


    cur.execute(
        """
        SELECT stat_date
        FROM financial_profit
        WHERE code=?
        """,
        (code,)
    )


    data = cur.fetchall()


    conn.close()


    return {
        x[0]
        for x in data
    }



# =========================
# 东方财富代码
# =========================

def em_code(code):

    if code.startswith("6"):

        return "SH" + code

    else:

        return "SZ" + code



# =========================
# 请求分页
# =========================

def fetch_page(code,page):


    params = {

        "type": "0",

        "code": em_code(code),

        "pageNumber": page,

        "pageSize": 50

    }


    try:

        r=requests.get(

            URL,

            params=params,

            headers=HEADERS,

            timeout=10

        )


        return r.json()


    except Exception as e:


        print(
            "接口异常",
            code,
            e
        )

        return None



# =========================
# 下载单股票
# =========================

def download_one(code):


    first = fetch_page(
        code,
        1
    )


    if not first:

        return -1



    if "data" not in first:

        return 0



    pages = first.get(
        "pages",
        1
    )


    all_rows = []


    all_rows.extend(
        first["data"]
    )


    # 分页

    for page in range(
        2,
        pages + 1
    ):


        data = fetch_page(
            code,
            page
        )


        if data and data.get("data"):

            all_rows.extend(
                data["data"]
            )


        time.sleep(0.1)



    exists = existing_dates(code)


    insert=[]


    for row in all_rows:


        stat=row.get(
            "REPORTDATE"
        )


        if not stat:

            continue


        stat=stat[:10]


        if stat in exists:

            continue



        insert.append(

            (

            code,


            row.get(
                "NOTICE_DATE"
            ),


            stat,


            row.get(
                "WEIGHTAVG_ROE"
            ),


            None,


            row.get(
                "XSMLL"
            ),


            row.get(
                "PARENT_NETPROFIT"
            ),


            row.get(
                "BASIC_EPS"
            ),


            row.get(
                "TOTAL_OPERATE_INCOME"
            ),


            None,


            None

            )

        )



    if not insert:


        print(
            code,
            "财务完整",
            "已有:",
            len(all_rows)
        )


        return 0



    conn=conn_db()

    cur=conn.cursor()


    cur.executemany(

        """
        INSERT OR IGNORE INTO financial_profit

        (

        code,

        pub_date,

        stat_date,


        roe_avg,

        np_margin,

        gp_margin,


        net_profit,

        eps_ttm,

        main_business_revenue,


        total_share,

        liqa_share

        )

        VALUES

        (?,?,?,?,?,?,?,?,?,?,?)

        """,

        insert

    )


    conn.commit()

    conn.close()



    print(

        code,

        "新增:",

        len(insert),

        "总历史:",

        len(all_rows)

    )


    return len(insert)



# =========================
# 主程序
# =========================

def main():


    init_table()


    stocks=get_stocks()



    if TEST_LIMIT:

        stocks=stocks[:TEST_LIMIT]



    print(
        "股票数量:",
        len(stocks)
    )



    ok=0
    skip=0
    fail=0



    for i,code in enumerate(
        stocks,
        1
    ):


        print(
            f"[{i}/{len(stocks)}]",
            code
        )


        try:

            result=download_one(code)


            if result>0:

                ok+=1


            elif result==0:

                skip+=1


            else:

                fail+=1



        except Exception as e:


            print(
                "失败:",
                code,
                e
            )

            fail+=1



        time.sleep(
            0.2
        )



    print()

    print(
        "财务下载完成"
    )

    print(
        "新增:",
        ok,
        "完整:",
        skip,
        "失败:",
        fail
    )



if __name__=="__main__":

    main()