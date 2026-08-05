import baostock as bs
import pandas as pd
import time
import random
import atexit
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

from data.writer import insert_dataframe, execute_sql


TEST_LIMIT = 5


def init_worker():
    time.sleep(random.randint(5, 15))

    for i in range(5):
        lg = bs.login()

        if lg.error_code == "0":
            atexit.register(bs.logout)
            print("worker 登录成功", flush=True)
            return

        print("Baostock登录失败", i + 1, lg.error_msg, flush=True)
        time.sleep(60)

    raise Exception("Baostock登录失败5次")


def convert_code(code):
    if str(code).startswith(
        ("600", "601", "603", "605", "688", "689")
    ):
        return "sh." + str(code)

    return "sz." + str(code)


def save_log(code, status, message):
    execute_sql(
        """
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
            :code,
            'daily_qfq',
            :status,
            :message,
            :time
        )
        """,
        {
            "code": code,
            "status": status,
            "message": message,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )


def already_done(code):
    rows = execute_sql(
        """
        SELECT status
        FROM download_log
        WHERE code=:code
        AND data_type='daily_qfq'
        """,
        {
            "code": code
        }
    ).fetchall()

    return bool(
        rows and rows[0][0] == "success"
    )


def download_one(stock):

    code, ipo_date = stock

    if not ipo_date:
        raise Exception("IPO日期为空")

    start_date = str(ipo_date)[:10]

    today = datetime.now().strftime("%Y-%m-%d")

    if start_date >= today:
        raise Exception(
            f"IPO日期异常:{start_date}"
        )

    rs = bs.query_history_k_data_plus(
        convert_code(code),
        "date,open,high,low,close,volume,amount",
        start_date=start_date,
        end_date=today,
        frequency="d",
        adjustflag="2"
    )

    if rs.error_code != "0":
        raise Exception(rs.error_msg)

    data = []

    while rs.next():
        data.append(
            rs.get_row_data()
        )

    if not data:
        raise Exception("无数据")

    df = pd.DataFrame(
        data,
        columns=rs.fields
    )

    df["code"] = code

    insert_dataframe(
        df,
        "daily_price_qfq"
    )

    return len(df)


def worker(stock):

    code = stock[0]

    try:
        count = download_one(stock)

        save_log(
            code,
            "success",
            f"daily_qfq {count}"
        )

        return (
            code,
            count,
            "success"
        )

    except Exception as e:

        save_log(
            code,
            "failed",
            str(e)
        )

        return (
            code,
            0,
            "failed"
        )


def main():

    rows = execute_sql(
        """
        SELECT code, ipo_date
        FROM stock_basic
        WHERE status='1'
        ORDER BY code
        """
    ).fetchall()

    stocks = [
        (x[0], x[1])
        for x in rows
    ]

    todo = [
        x for x in stocks
        if not already_done(x[0])
    ]

    if TEST_LIMIT:
        todo = todo[:TEST_LIMIT]

    print(
        "QFQ股票数量:",
        len(stocks)
    )

    print(
        "待下载:",
        len(todo)
    )

    if not todo:
        print("没有需要下载的股票")
        return

    success = 0
    failed = 0

    with ProcessPoolExecutor(
        max_workers=4,
        initializer=init_worker
    ) as executor:

        futures = [
            executor.submit(worker, stock)
            for stock in todo
        ]

        for i, future in enumerate(
            as_completed(futures),
            1
        ):

            result = future.result()

            if result[2] == "success":
                success += 1
            else:
                failed += 1

            print(
                i,
                "/",
                len(todo),
                result,
                flush=True
            )

    print(
        "完成 成功:",
        success,
        "失败:",
        failed
    )


if __name__ == "__main__":
    main()
