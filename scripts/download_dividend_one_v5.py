import sys

import baostock as bs
import pandas as pd

from data.writer import insert_ignore


def convert_code(code):

    if code.startswith(("600","601","603","605","688")):
        return "sh." + code

    return "sz." + code


def download_dividend(code):

    rows = []

    bs.login()

    for year in range(2000, 2026):

        rs = bs.query_dividend_data(
            code=convert_code(code),
            year=str(year),
            yearType="report"
        )

        while rs.next():

            row = rs.get_row_data()

            rows.append(
                {
                    "code": code,
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

    bs.logout()

    if rows:
        insert_ignore(
            pd.DataFrame(rows),
            "dividend"
        )


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("usage: python -m scripts.download_dividend_one_v5 000001")
        sys.exit(1)

    download_dividend(sys.argv[1])
