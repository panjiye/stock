import baostock as bs


def main():

    lg = bs.login()

    if lg.error_code != "0":
        print(lg.error_msg)
        return


    rs = bs.query_dividend_data(
        code="sh.600519",
        year="2025",
        yearType="report"
    )


    print(rs.error_code)
    print(rs.error_msg)


    while rs.next():
        print(rs.get_row_data())


    bs.logout()


if __name__ == "__main__":
    main()