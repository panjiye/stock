import sqlite3
import baostock as bs
import pandas as pd

from sqlalchemy import create_engine, text
from datetime import datetime

import os
import atexit

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

    lg = bs.login()

    if lg.error_code != "0":

        raise Exception(
            lg.error_msg
        )


    # 进程退出自动logout

    atexit.register(
        bs.logout
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
            "daily_raw",
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
        AND data_type='daily_raw'
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
        adjustflag="3"
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


    df=pd.DataFrame(
        data,
        columns=rs.fields
    )


    df["code"]=code



    with engine.begin() as conn:

        conn.execute(
            text(
            """
            DELETE FROM daily_price_raw
            WHERE code=:code
            """
            ),
            {
                "code":code
            }
        )


    check = pd.read_sql(
        f"""
        SELECT count(*)
        FROM daily_price_qfq
        WHERE code='{code}'
        """,
        engine
    )

    if check.iloc[0,0] == 0:
        raise Exception("写入失败")

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
            f"daily_raw {count}"
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

    conn=sqlite3.connect(DB)

    cursor=conn.cursor()


    cursor.execute(
        """
        SELECT code, ipo_date
        FROM stock_basic
        WHERE status='1'
        """
    )


    stocks=[
        (x[0],x[1])
        for x in cursor.fetchall()
    ]

    # 测试
    #stocks = stocks[:1100]

    conn.close()
    print(
        "股票数量:",
        len(stocks)
    )



    todo=[]


    for stock in stocks:

        if not already_done(
            stock[0]
        ):

            todo.append(stock)



    print(
        "待下载:",
        len(todo)
    )



    if len(todo)==0:

        print(
            "没有需要下载的股票"
        )

        return



    workers=4



    success=0

    finished=0

    total=len(todo)



    with ProcessPoolExecutor(
        max_workers=workers,
        initializer=init_worker
    ) as executor:


        futures=[]


        for stock in todo:


            futures.append(
                executor.submit(
                    worker,
                    stock
                )
            )



        for future in as_completed(futures):


            result=future.result()


            finished += 1


            if result[2]=="success":

                success += 1



            print(
                finished,
                "/",
                total,
                result,
                flush=True
            )



    print(
        "完成:",
        success
    )




if __name__=="__main__":

    main()