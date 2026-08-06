import sqlite3
import baostock as bs
from datetime import datetime


DB = "database/stock.db"


def save_dividend(data):

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO dividend
    (
        code,
        regist_date,
        declare_date,
        pay_date,
        ex_date,

        cash_before_tax,
        cash_after_tax,

        bonus_share,
        transfer_share,

        dividend_info
    )
    VALUES
    (
        ?,?,?,?,?,?,?,?,?,?
    )
    """, data)

    conn.commit()
    conn.close()


def download_dividend(code="sh.600519", year="2025"):

    lg = bs.login()

    if lg.error_code != "0":
        print("登录失败:", lg.error_msg)
        return


    print("开始下载:", code)


    rs = bs.query_dividend_data(
        code=code,
        year=year,
        yearType="report"
    )


    if rs.error_code != "0":
        print(rs.error_msg)
        bs.logout()
        return


    count = 0


    while rs.next():

        row = rs.get_row_data()


        data = (

            code.replace(
                "sh.",
                ""
            ).replace(
                "sz.",
                ""
            ),

            row[2],      # regist_date

            row[3],      # declare_date

            row[4],      # pay_date

            row[6],      # ex_date


            float(row[9]) if row[9] else 0,

            float(row[10].split("或")[0])
            if row[10] else 0,


            float(row[11])
            if row[11] else 0,


            0,


            row[12]

        )


        save_dividend(data)

        count += 1


    print("写入记录:", count)


    bs.logout()



if __name__ == "__main__":

    download_dividend(
        "sh.600519",
        "2025"
    )