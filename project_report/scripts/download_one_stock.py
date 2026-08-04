import baostock as bs
import pandas as pd
import sqlite3
from sqlalchemy import create_engine, text
import os
from datetime import datetime


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


db_file = os.path.join(
    BASE_DIR,
    "database",
    "stock.db"
)


engine = create_engine(
    f"sqlite:///{db_file}"
)


# =========================
# 下载日志
# =========================

def write_log(code, status, message):

    sql = """
    INSERT INTO download_log
    (
        code,
        status,
        message,
        update_time
    )
    VALUES
    (
        ?,
        ?,
        ?,
        ?
    )
    ON CONFLICT(code)
    DO UPDATE SET

        status=excluded.status,
        message=excluded.message,
        update_time=excluded.update_time
    """


    conn = sqlite3.connect(db_file)

    cursor = conn.cursor()

    cursor.execute(
        sql,
        (
            code,
            status,
            message,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
    )


    conn.commit()

    conn.close()



# =========================
# 股票代码转换
# =========================

def get_bs_code(code):

    if code.startswith(
        ("6", "688")
    ):
        return "sh." + code

    else:
        return "sz." + code



# =========================
# 查询数据库最新日期
# =========================

def get_last_date(code):

    sql = text("""
        SELECT MAX(date)
        FROM daily_price
        WHERE code=:code
    """)


    with engine.connect() as conn:

        result = conn.execute(
            sql,
            {
                "code": code
            }
        )

        last_date = result.fetchone()[0]


    return last_date



# =========================
# 下载单只股票
# =========================

def download_stock(code):


    print(
        f"开始下载 {code}"
    )


    try:

        bs_code = get_bs_code(code)


        # 登录

        login = bs.login()


        if login.error_code != "0":

            raise Exception(
                login.error_msg
            )


        last_date = get_last_date(code)


        print(
            "数据库最后日期:",
            last_date
        )


        if last_date:

            start_date = last_date

        else:

            start_date = "2000-01-01"



        rs = bs.query_history_k_data_plus(
            bs_code,
            "date,open,high,low,close,volume,amount",
            start_date=start_date,
            end_date=datetime.today().strftime(
                "%Y-%m-%d"
            ),
            frequency="d",
            adjustflag="2"
        )


        if rs.error_code != "0":

            raise Exception(
                rs.error_msg
            )



        data = []


        while rs.next():

            data.append(
                rs.get_row_data()
            )



        if len(data) == 0:

            write_log(
                code,
                "success",
                "无新数据"
            )

            print(
                f"{code} 无新数据"
            )

            return True



        df = pd.DataFrame(
            data,
            columns=rs.fields
        )


        # 日期统一

        df["date"] = (
            df["date"]
            .astype(str)
        )


        # 删除已有日期

        if last_date:

            df = df[
                df["date"] > last_date
            ]


        print(
            "过滤后剩余数据:",
            len(df)
        )



        if len(df) == 0:

            print(
                f"{code} 已经是最新"
            )


            write_log(
                code,
                "success",
                "已经是最新"
            )

            return True



        # 增加股票代码

        df["code"] = code



        # 防止重复

        df = df.drop_duplicates(
            subset=[
                "code",
                "date"
            ]
        )


        print(
            "去重后:",
            len(df)
        )



        df.to_sql(
            "daily_price",
            engine,
            if_exists="append",
            index=False
        )


        print(
            f"{code} 保存完成 {len(df)} 条"
        )


        write_log(
            code,
            "success",
            f"新增{len(df)}条"
        )


        return True



    except Exception as e:


        print(
            "错误:",
            e
        )


        write_log(
            code,
            "failed",
            str(e)
        )


        return False



    finally:

        try:

            bs.logout()

        except:

            pass




# =========================
# 测试
# =========================

if __name__ == "__main__":


    download_stock(
        "600519"
    )


    download_stock(
        "000001"
    )