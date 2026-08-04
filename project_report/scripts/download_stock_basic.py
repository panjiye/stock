import baostock as bs
import pandas as pd
from sqlalchemy import create_engine
import os


# ======================
# 项目根目录
# ======================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ======================
# 数据库路径
# ======================

db_file = os.path.join(
    BASE_DIR,
    "database",
    "stock.db"
)


engine = create_engine(
    f"sqlite:///{db_file}"
)


print("正在获取股票基础信息...")


# ======================
# 登录 Baostock
# ======================

lg = bs.login()

if lg.error_code != "0":
    raise Exception(
        lg.error_msg
    )


# ======================
# 查询股票基础信息
# ======================

rs = bs.query_stock_basic()


data = []


while rs.next():

    data.append(
        rs.get_row_data()
    )


bs.logout()


# ======================
# 创建 DataFrame
# ======================

df = pd.DataFrame(
    data,
    columns=rs.fields
)


print("原始数据数量:", len(df))


# ======================
# 只保留股票
#
# type:
# 1 股票
# 2 指数
# ======================

df = df[
    df["type"] == "1"
]


# ======================
# 字段整理
# ======================

df = df.rename(
    columns={
        "code_name": "name",
        "ipoDate": "ipo_date",
        "outDate": "out_date"
    }
)


# ======================
# 去掉 Baostock 前缀
#
# sh.600519 -> 600519
# sz.000001 -> 000001
# ======================

df["code"] = (
    df["code"]
    .str.split(".")
    .str[-1]
)


# ======================
# 保存字段
# ======================

df = df[
    [
        "code",
        "name",
        "ipo_date",
        "out_date",
        "type",
        "status"
    ]
]


print(df.head())

print(
    "股票数量:",
    len(df)
)


# ======================
# 写入数据库
# ======================

df.to_sql(
    "stock_basic",
    engine,
    if_exists="replace",
    index=False
)


print("stock_basic 更新完成")
print(db_file)