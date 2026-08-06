import baostock as bs
import sqlite3
import time
import random

from datetime import datetime


# ======================
# 配置
# ======================

DB = "database/stock.db"


# 从上市以来开始
DEFAULT_START_YEAR = 1990

CURRENT_YEAR = datetime.now().year


# None = 全市场
LIMIT = 50



# ======================
# 数据库连接
# ======================

conn = sqlite3.connect(
    DB,
    timeout=60
)

cursor = conn.cursor()



# ======================
# 股票代码转换
# ======================

def convert_bs_code(code):

    code = str(code)


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


    return "sz." + code




# ======================
# 安全转换
# ======================

def safe_float(value):

    if value == "":

        return None

    try:

        return float(value)

    except:

        return None




# ======================
# 获取股票已有财务季度
# ======================

def get_existing_quarters(code):


    cursor.execute(
        """
        SELECT stat_date

        FROM financial_profit

        WHERE code=?

        """,
        (
            code,
        )
    )


    rows = cursor.fetchall()


    result = set()


    for row in rows:


        stat_date = row[0]


        if not stat_date:

            continue


        try:


            year = int(
                stat_date[:4]
            )


            month = int(
                stat_date[5:7]
            )


            if month <= 3:

                quarter = 1


            elif month <= 6:

                quarter = 2


            elif month <= 9:

                quarter = 3


            else:

                quarter = 4



            result.add(
                (
                    year,
                    quarter
                )
            )


        except:

            continue



    return result





# ======================
# 获取缺失季度
# ======================

def get_missing_quarters(code):


    exists = get_existing_quarters(
        code
    )


    expected = []


    for year in range(
        DEFAULT_START_YEAR,
        CURRENT_YEAR + 1
    ):


        for quarter in range(
            1,
            5
        ):


            expected.append(
                (
                    year,
                    quarter
                )
            )



    missing = [

        x for x in expected

        if x not in exists

    ]


    return (
        exists,
        missing
    )




# ======================
# 保存日志
# ======================

def save_log(
        code,
        status,
        message
):


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
            "profit",
            status,
            message,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

    )





# ======================
# 获取股票列表
# ======================


cursor.execute(
    """
    SELECT code

    FROM stock_basic

    WHERE status='1'

    ORDER BY code

    """
)


stocks = [

    x[0]

    for x in cursor.fetchall()

]



if LIMIT:


    stocks = stocks[:LIMIT]



print(
    "股票数量:",
    len(stocks)
)

print(
    "财务范围:",
    DEFAULT_START_YEAR,
    "-",
    CURRENT_YEAR
)
# ======================
# Baostock 登录
# ======================


for i in range(5):


    time.sleep(
        random.randint(3,10)
    )


    lg = bs.login()


    if lg.error_code == "0":


        print(
            "Baostock登录成功"
        )

        break


    else:


        print(
            "登录失败:",
            lg.error_msg
        )


        time.sleep(30)



else:


    raise Exception(
        "Baostock登录失败"
    )





# ======================
# 下载统计
# ======================


success = 0
skip = 0
failed = 0





# ======================
# 开始循环股票
# ======================


for index, code in enumerate(stocks):


    print(
        f"[{index+1}/{len(stocks)}]",
        code,
        flush=True
    )



    try:


        exists, missing = get_missing_quarters(
            code
        )


        print(
            "已有季度:",
            len(exists),
            "/",
            len(exists)+len(missing),
            flush=True
        )



        if not missing:


            print(
                "财务完整，跳过",
                flush=True
            )


            skip += 1


            continue




        print(
            "缺失季度:",
            missing,
            flush=True
        )



        bs_code = convert_bs_code(
            code
        )


        new_count = 0




        # ======================
        # 只下载缺失季度
        # ======================


        for year, quarter in missing:



            print(
                "查询:",
                code,
                year,
                "Q",
                quarter,
                flush=True
            )



            rs = bs.query_profit_data(

                code=bs_code,

                year=year,

                quarter=quarter

            )



            if rs.error_code != "0":


                print(
                    "查询失败:",
                    rs.error_msg,
                    flush=True
                )


                continue




            while rs.next():


                row = rs.get_row_data()



                cursor.execute(

                    """

                    INSERT OR IGNORE INTO financial_profit

                    (

                        code,

                        pub_date,

                        stat_date,

                        roe_avg,

                        np_margin,

                        gp_margin,

                        net_profit,

                        eps_ttm,

                        main_business_revenue,

                        total_share,

                        liqa_share

                    )


                    VALUES

                    (?,?,?,?,?,?,?,?,?,?,?)

                    """,

                    (

                        code,

                        row[1],

                        row[2],

                        safe_float(row[3]),

                        safe_float(row[4]),

                        safe_float(row[5]),

                        safe_float(row[6]),

                        safe_float(row[7]),

                        safe_float(row[8]),

                        safe_float(row[9]),

                        safe_float(row[10])

                    )

                )



                new_count += 1



            # ======================
            # 每季度立即保存
            # ======================

            conn.commit()



            time.sleep(
                random.uniform(
                    0.05,
                    0.2
                )
            )





        save_log(

            code,

            "success",

            f"新增 {new_count}"

        )


        conn.commit()



        print(

            "完成:",

            code,

            "新增:",

            new_count,

            flush=True

        )



        success += 1




    except Exception as e:



        print(

            "失败:",

            code,

            e,

            flush=True

        )


        save_log(

            code,

            "failed",

            str(e)

        )


        conn.commit()



        failed += 1





    # 股票之间随机等待

    time.sleep(

        random.randint(
            2,
            5
        )

    )





    if (index+1)%100 == 0:


        print(

            "进度:",

            index+1,

            "/",

            len(stocks),

            "成功:",

            success,

            "跳过:",

            skip,

            "失败:",

            failed,

            flush=True

        )







# ======================
# 退出
# ======================


bs.logout()


conn.close()



print(
    "财务批量下载完成"
)


print(

    "成功:",

    success,

    "跳过:",

    skip,

    "失败:",

    failed

)