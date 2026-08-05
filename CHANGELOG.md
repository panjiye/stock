# CHANGELOG

# V5 数据层迁移

日期：

2026-08-05


## 完成

### Writer层建设

新增：

- data.writer统一写入层
- dataframe批量写入
- upsert/ignore写入支持


### 下载脚本迁移

完成：

- download_index
- download_industry
- dividend系列脚本
- one_stock下载脚本


新增：

- scripts/download_dividend_all_v5.py
- scripts/download_dividend_one_v5.py
- scripts/download_one_stock_v5.py
- scripts/migrate_writer_v5.py
- scripts/migrate_dividend_writer_v5.py


## Git提交记录

v5-dev:

- 5c68e57 migrate download_index
- 691bdb2 migrate download_industry
- 3b1e210 add dataframe upsert writer
- 268df88 migrate dividend downloader
- 9427bd0 add writer migration tools


# 下一阶段

继续迁移：

- download_profit_all.py
- download_daily_qfq_all.py
- download_financial_all_v2.py


目标：

所有业务脚本不直接操作sqlite。


# Changelog


## v5-dev

日期：

2026-08-05


## Added


新增：

- data.writer 写入抽象层
- migration 工具


新增脚本：

- download_dividend_all_v5.py
- download_dividend_one_v5.py
- download_one_stock_v5.py
- migrate_writer_v5.py
- migrate_dividend_writer_v5.py


---


## Changed


### 数据库访问重构


迁移：

download_index.py


download_industry.py


download_dividend 系列


由：

sqlite3


改为：

SQLAlchemy + Writer Layer



---


## Fixed


修复：

- writer 层缺少 insert_ignore 导致运行失败问题


---


## Next


计划：

继续迁移：

- profit
- daily
- financial

2026-08-05

Writer Layer 迁移阶段更新

完成以下模块数据库写入层迁移：

download_index.py

download_industry.py

dividend 系列

financial_profit 财务数据

daily_price_qfq 行情数据

统一使用 data.writer。

financial_profit 财报模块

确认数据来源：

东方财富 EastMoney。

历史问题：

部分百分比字段存在不同格式。

例如：

0.344620 表示 34.462%

10.57 表示 10.57%

处理方案：

analysis/financial_normalize.py 统一转换为小数形式。

daily_price_qfq

完成 Writer 迁移。

保留：

ProcessPoolExecutor 多进程

Baostock worker 登录模式

单股票任务模型

修复：

固定 end_date 导致新上市股票日期错误。

现在：

使用当前日期作为结束日期

增加 IPO 日期异常检测

测试：

001232 成功下载。