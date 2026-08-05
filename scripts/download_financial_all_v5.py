import requests
import time
import pandas as pd

from data.writer import insert_ignore, execute_sql


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

def init_table():
    # 表结构由 scripts/create_tables.py 管理
    return


def load_exists():

    rows = execute_sql(
        """
        SELECT code, stat_date
        FROM financial_profit
        """
    ).fetchall()

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

def save_rows(rows, exists):

    insert = []

    for item in rows:

        code = item.get("SECURITY_CODE")
        stat = item.get("REPORTDATE")

        if not code or not stat:
            continue

        stat = stat[:10]

        key = (code, stat)

        if key in exists:
            continue

        insert.append(
            {
                "code": code,
                "pub_date": item.get("NOTICE_DATE"),
                "stat_date": stat,
                "roe_avg": item.get("WEIGHTAVG_ROE"),
                "np_margin": item.get("XSMLL"),
                "gp_margin": item.get("XSMLL"),
                "net_profit": item.get("PARENT_NETPROFIT"),
                "eps_ttm": item.get("BASIC_EPS"),
                "main_business_revenue": item.get("TOTAL_OPERATE_INCOME"),
                "total_share": item.get("TOTAL_SHARE"),
                "liqa_share": item.get("LIQA_SHARE"),
            }
        )

    if not insert:
        return 0

    df = pd.DataFrame(insert)

    count = insert_ignore(
        df,
        "financial_profit"
    )

    return count


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
        1,
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