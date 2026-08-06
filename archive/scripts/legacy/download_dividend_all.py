import sqlite3
import baostock as bs
from datetime import datetime


DB = "database/stock.db"

def save_log(code, data_type, status, message):

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    cursor.execute("""
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
        ?,?,?,?,?
    )
    """,
    (
        code,
        data_type,
        status,
        message,
        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    ))

    conn.commit()
    conn.close()

def convert_code(code):

    if code.startswith(
        (
            "600",
            "601",
            "603",
            "605",
            "688"
        )
    ):
        return "sh." + code

    else:
        return "sz." + code



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


def download_one(code):

    count = 0


    for year in range(2000, 2026):

        rs = bs.query_dividend_data(
            code=code,
            year=str(year),
            yearType="report"
        )


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
                row[2],
                row[3],
                row[4],
                row[6],

                float(row[9])
                if row[9] else 0,


                float(
                    row[10].split("或")[0]
                )
                if row[10] else 0,


                float(row[11])
                if row[11] else 0,


                0,


                row[12]

            )


            save_dividend(data)

            count += 1


    return count


def main():

    bs.login()


    conn = sqlite3.connect(DB)

    cursor = conn.cursor()


    cursor.execute("""
    SELECT code
    FROM stock_basic
    WHERE status='1'
    """)


    stocks = cursor.fetchall()
    # ==================================================
    # ================  注意 — IMPORTANT  ==============
    # = 此处临时限制为 20 支股票以便测试与调试。     =
    # = 若要下载全部股票，请删除或注释掉下一行。   =
    # ==================================================
    stocks = stocks[:20] 

    # 已经成功下载的股票
    cursor.execute("""
    SELECT code
    FROM download_log
    WHERE data_type='dividend'
    AND status='success'
    """)

    finished = {
        row[0]
        for row in cursor.fetchall()
    }


    stocks = [
        row
        for row in stocks
        if row[0] not in finished
    ]


    conn.close()


    total = len(stocks)

    print(
        "股票数量:",
        total
    )


    success = 0


    for i, row in enumerate(stocks):

        raw_code = row[0]

        bs_code = convert_code(raw_code)


        try:

            count = download_one(
                bs_code
            )
            if count > 0:
                save_log(
                    raw_code,
                    "dividend",
                    "success",
                    f"dividend {count}"
                )

            else:

                save_log(
                    raw_code,
                    "dividend",
                    "empty",
                    "no dividend"
                )

            if count > 0:

                success += 1

                save_log(
                    raw_code,
                    "dividend",
                    "success",
                    f"dividend {count}"
                )

            else:

                save_log(
                    raw_code,
                    "dividend",
                    "empty",
                    "no dividend"
                )


            print(
                i+1,
                "/",
                total,
                bs_code,
                "分红:",
                count
            )


        except Exception as e:

            print(
                "失败:",
                bs_code,
                e
            )


            save_log(
                raw_code,
                "dividend",
                "error",
                str(e)
            )

    print(
        "完成:",
        success
    )


    bs.logout()



if __name__ == "__main__":
    main()