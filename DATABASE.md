# 数据库说明


数据库：

database/stock.db


数据库类型：

SQLite



# 行情数据


## daily_price_qfq

股票前复权日线。


字段：

date

code

open

high

low

close

volume

amount


用途：

主要回测数据。


---

## index_price

指数行情。


示例：

000300.SH


用途：

市场环境过滤。



# 技术数据


## daily_indicator

技术指标。


包含：

MA60

等指标。


用途：

策略判断。


---

## technical_factor

技术因子。


用途：

技术评分。


---

## technical_rank

技术排名。



# 财务数据


## financial_profit

利润数据。


## financial_factor

财务指标。


## financial_profit_normalized

标准化财务数据。


## valuation_factor

估值因子。



# 综合数据


## factor_score

最终因子评分。


## stock_pool

股票池。


# 数据原则


所有模块：

禁止直接读取原始文件。


统一：

数据库
↓
data.query
↓
策略模块
