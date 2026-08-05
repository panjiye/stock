import time
from datetime import datetime

import baostock as bs
import pandas as pd

from data.writer import insert_ignore, insert_replace, execute_sql


def save_log(code, data_type, status, message):
    sql = """
    INSERT OR REPLACE INTO download_log
    (
        code,
        data_type,
        status,
        message,
        update_time
    )
    VALUES
    (
        :code,:data_type,:status,:message,:update_time
    )
    """

    execute_sql(
        sql,
        {
            "code": code,
            "data_type": data_type,
            "status": status,
            "message": message,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )


def convert_code(code):
    if code.startswith(("600","601","603","605","688")):
        return "sh." + code
    return "sz." + code


def download_one(code):

    rows = []

    for year in range(2000, 2026):

        rs = bs.query_dividend_data(
            code=code,
            year=str(year),
            yearType="report"
        )

        while rs.next():

            row = rs.get_row_data()

            rows.append(
                {
                    "code": code.replace("sh.","").replace("sz.",""),
                    "regist_date": row[2],
                    "declare_date": row[3],
                    "pay_date": row[4],
                    "ex_date": row[6],
                    "cash_before_tax": float(row[9]) if row[9] else 0,
                    "cash_after_tax": float(row[10].split("或")[0]) if row[10] else 0,
                    "bonus_share": float(row[11]) if row[11] else 0,
                    "transfer_share": 0,
                    "dividend_info": row[12]
                }
            )

    if not rows:
        return 0

    df = pd.DataFrame(rows)

    insert_ignore(
        df,
        "dividend"
    )

    return len(df)


def main():

    bs.login()

    print("请确认股票池读取逻辑后接入 stock_basic")

    bs.logout()


if __name__ == "__main__":
    main()
