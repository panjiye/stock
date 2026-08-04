import baostock as bs
import pandas as pd
from sqlalchemy import create_engine
import os


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


# ======================
# 指数代码
# ======================

code = "000300"

bs_code = "sh." + code


print(
    f"开始下载指数 {code}"
)


# 登录

lg = bs.login()


if lg.error_code != "0":

    raise Exception(
        lg.error_msg
    )


# 查询

rs = bs.query_history_k_data_plus(

    bs_code,

    "date,open,high,low,close,volume,amount",

    start_date="2005-01-01",

    end_date="2026-08-01",

    frequency="d",

    adjustflag="2"

)


data=[]


while rs.next():

    data.append(
        rs.get_row_data()
    )


bs.logout()



df = pd.DataFrame(
    data,
    columns=rs.fields
)


print(
    "数据量:",
    len(df)
)


# 增加代码

df["code"] = "000300.SH"


df.to_sql(

    "index_price",

    engine,

    if_exists="append",

    index=False

)


print(
    "保存完成"
)