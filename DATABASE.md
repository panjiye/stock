# 数据库说明

数据库：

database/stock.db

类型：

SQLite


# 数据访问原则

V5:

写入：

scripts

↓

data.writer

↓

SQLite


读取：

SQLite

↓

data.query


禁止业务代码直接 sqlite3.connect。


---

# 主要数据表


## 行情

daily_price_qfq

前复权行情。


index_price

指数行情。


用途：

市场环境过滤。


## 股票基础

stock_basic

股票列表。


stock_pool

股票池。


## 财务

financial_profit

利润数据。


financial_factor

财务因子。


valuation_factor

估值因子。


## 综合

factor_score

综合评分。


---

# 当前数据库迁移状态

已完成：

- 指数数据写入迁移
- 行业数据写入迁移
- 分红数据写入迁移


待完成：

- financial_profit 写入迁移
- daily_price_qfq 写入迁移
