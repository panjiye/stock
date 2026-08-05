# Database

更新时间：2026-08-05


数据库：

database/stock.db


当前数据库类型：

SQLite


访问方式：

SQLAlchemy engine


---


# 写入规范


从 v5 开始：


禁止：

sqlite3.connect()

cursor.execute()

直接 INSERT


统一：

data.writer


---


# 已确认表


## dividend


字段：

- code
- regist_date
- declare_date
- pay_date
- ex_date
- cash_before_tax
- cash_after_tax
- bonus_share
- transfer_share
- dividend_info


唯一索引：

idx_dividend_unique

(code, ex_date)


---


## download_log


字段：

- code
- data_type
- status
- message
- update_time


作用：

记录下载状态。


---


## financial_profit


状态：

正在迁移。


---


# 数据写入策略


行情类：

insert_ignore


财务类：

insert_ignore


状态日志：

insert_replace

