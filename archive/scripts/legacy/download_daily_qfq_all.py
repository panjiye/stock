import sqlite3
import baostock as bs
import pandas as pd

from sqlalchemy import create_engine, text
from datetime import datetime

import os
import atexit
import time
import random

from concurrent.futures import (
    ProcessPoolExecutor,
    as_completed
)


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DB = os.path.join(
    BASE_DIR,
    "database",
    "stock.db"
)


engine = create_engine(
    f"sqlite:///{DB}"
)



# ==================================================
# worker 初始化
# 一个进程只登录一次
# ==================================================

def init_worker():


    time.sleep(
        random.randint(5,30)
    )


    for i in range(5):

        lg = bs.login()


        if lg.error_code == "0":

            atexit.register(
                bs.logout
            )

            print(
                "worker 登录成功",
                flush=True
            )

            return


        print(
            "Baostock登录失败，第",
            i+1,
            "次重试",
            lg.error_msg,
            flush=True
        )


        time.sleep(60)



    raise Exception(
        "Baostock登录失败5次"
    )



# ==================================================
# 股票代码转换
# ==================================================

def convert_code(code):


    if code.startswith(
        (
            "600",
            "601",
            "603",
            "605",
            "688",
            "689"
        )
    ):

        return "sh." + code


    else:

        return "sz." + code




# ==================================================
# 保存日志
# ==================================================

def save_log(
        code,
        status,
        message
):


    conn = sqlite3.connect(
        DB,
        timeout=60
    )


    cursor = conn.cursor()


    cursor.execute(
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
        (?,?,?,?,?)
        """,
        (
            code,
            "daily_qfq",
            status,
            message,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )


    conn.commit()

    conn.close()





# ==================================================
# 判断是否已经完成
# ==================================================

def already_done(code):


    conn = sqlite3.connect(
        DB,
        timeout=60
    )


    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT status
        FROM download_log
        WHERE code=?
        AND data_type='daily_qfq'
        """,
        (code,)
    )


    row = cursor.fetchone()


    conn.close()



    return (
        row
        and row[0]=="success"
    )





# ==================================================
# 单股票下载
# ==================================================

def download_one(stock):


    code, ipo_date = stock


    bs_code = convert_code(code)



    rs = bs.query_history_k_data_plus(
        bs_code,
        "date,open,high,low,close,volume,amount",
        start_date=ipo_date,
        end_date="2026-08-01",
        frequency="d",
        adjustflag="2"
    )



    data=[]



    while rs.next():

        data.append(
            rs.get_row_data()
        )



    if len(data)==0:


        raise Exception(
            "无数据"
        )



    df = pd.DataFrame(
        data,
        columns=rs.fields
    )


    df["code"] = code





    # with engine.begin() as conn:


    #     conn.execute(
    #         text(
    #         """
    #         DELETE FROM daily_price_qfq
    #         WHERE code=:code
    #         """
    #         ),
    #         {
    #             "code":code
    #         }
    #     )




    df.to_sql(
        "daily_price_qfq",
        engine,
        if_exists="append",
        index=False
    )



    return len(df)





# ==================================================
# worker
# 一个任务 = 一只股票
# ==================================================

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
# ==================================================
# 主程序
# ==================================================

def main():

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT code, ipo_date
        FROM stock_basic
        WHERE status='1'
        """
    )


    stocks = [
        (x[0], x[1])
        for x in cursor.fetchall()
    ]


    conn.close()


    print(
        "QFQ股票数量:",
        len(stocks)
    )



    todo = []


    for stock in stocks:

        if not already_done(
            stock[0]
        ):

            todo.append(stock)



    print(
        "待下载:",
        len(todo)
    )



    if len(todo) == 0:

        print(
            "没有需要下载的股票"
        )

        return



    # 同时运行进程数量
    # Baostock限制比较严格
    workers = 4


    # 每批提交数量
    batch_size = 100



    success = 0

    finished = 0

    total = len(todo)



    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=init_worker
    ) as executor:



        for start in range(
            0,
            total,
            batch_size
        ):


            batch = todo[
                start:
                start + batch_size
            ]



            print(
                "开始批次:",
                start,
                "-",
                start + len(batch),
                flush=True
            )



            futures = []



            for stock in batch:


                futures.append(
                    executor.submit(
                        worker,
                        stock
                    )
                )



            for future in as_completed(
                futures
            ):


                result = future.result()


                finished += 1



                if result[2] == "success":

                    success += 1



                print(
                    finished,
                    "/",
                    total,
                    result,
                    flush=True
                )



            # 每批结束休息
            # 避免触发黑名单

            time.sleep(
                random.randint(
                    20,
                    40
                )
            )



    print(
        "完成:",
        success
    )
if __name__=="__main__":

    main()