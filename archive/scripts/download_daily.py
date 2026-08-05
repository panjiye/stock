import baostock as bs
import pandas as pd
from sqlalchemy import create_engine
import os


# 项目根目录
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# 数据库路径
db_file = os.path.join(
    BASE_DIR,
    "database",
    "stock.db"
)


engine = create_engine(
    f"sqlite:///{db_file}"
)


# 测试股票
code = "600519"

# Baostock格式
bs_code = "sh." + code


print(f"开始下载 {code}")


# 登录
lg = bs.login()

if lg.error_code != "0":
    raise Exception(lg.error_msg)


# 查询历史行情
rs = bs.query_history_k_data_plus(
    bs_code,
    "date,open,high,low,close,volume,amount",
    start_date="2000-01-01",
    end_date="2026-08-01",
    frequency="d",
    adjustflag="2"
)

data = []

if rs.error_code != "0":
    print(rs.error_msg)
    bs.logout()
    exit()


while rs.next():
    data.append(
        rs.get_row_data()
    )
bs.logout()


# 转DataFrame

df = pd.DataFrame(
    data,
    columns=rs.fields
)


print(df.head())

print("数据量:", len(df))


# 添加股票代码

df["code"] = code


# 写入数据库

df.to_sql(
    "daily_price_qfq",
    engine,
    if_exists="append",
    index=False
)


print("保存完成")