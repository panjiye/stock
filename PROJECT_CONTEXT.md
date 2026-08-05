# A股量化研究系统项目上下文

更新时间：
2026-08-05

当前版本：
V4.2 Clean Baseline

开发分支：
v5-dev


# 1. 项目定位

这是一个个人 A 股量化研究系统。

目标不是开发单一策略，而是建立完整量化研究平台：

数据获取
→ 数据清洗
→ 数据库管理
→ 因子计算
→ 股票池生成
→ 评分选股
→ 策略交易
→ 回测验证
→ 风险控制
→ 绩效分析


长期目标：

建立类似小型量化研究框架。


# 2. 当前阶段

当前已经完成：

V4.2 策略验证阶段。

当前重点：

从 V4.2 迁移到 V5 架构。


V4.2 已经完成：

- 股票行情数据库
- 财务数据整理
- 技术指标计算
- 因子评分
- 股票池
- 回测框架
- 收益分析


# 3. 技术环境

操作系统：

Ubuntu Desktop 26.04 LTS


Python:

Python 3.14.4


虚拟环境：

.venv


主要依赖：

- pandas
- numpy
- sqlalchemy
- akshare
- baostock
- tushare
- requests


数据库：

SQLite

位置：

database/stock.db


# 4. 数据来源设计


## 行情数据

主要来源：

baostock


原因：

- 免费
- 稳定
- 历史数据完整
- 适合批量下载


主要表：

daily_price_qfq


用途：

股票日线回测。


## 财务数据

采用混合方式：

- 东方财富接口/爬虫
- Tushare
- AkShare


原因：

不同来源字段优势不同。


目标：

统一进入：

financial_profit

financial_factor

valuation_factor


# 5. 当前数据库


主要表：

## 行情

daily_price_qfq

复权日线行情


daily_price_hfq

后复权行情


daily_price_raw

原始行情


index_price

指数行情


## 股票基础

stock_basic

股票列表


stock_pool

股票池


## 技术因子

technical_factor

技术指标


technical_rank

技术排名


## 财务

financial_profit

财报数据


financial_factor

财务因子


financial_profit_normalized

标准化财务数据


## 综合评分

factor_score


# 6. 当前代码结构


stock/

analysis/

    query.py

数据库查询接口


strategy/

    market_filter.py

市场环境判断


    scoring.py

评分策略


    macd.py

    ma_cross.py


backtest/

    risk_stock_exit.py


scripts/

数据处理脚本


archive/

历史废弃代码


# 7. 当前已经完成的重要设计


## 数据访问统一

原则：

业务代码不能直接操作 sqlite。

通过：

data.query

访问数据库。


## 市场过滤

当前：

沪深300

条件：

close > MA60


作用：

判断市场环境。

避免熊市强行交易。


## Git版本管理


main:

V4.2稳定版本


v5-dev:

V5开发版本


tag:

v4.2-clean


# 8. 已废弃内容


以下不要继续维护：


risk_stock_exit_v2.py


原因：

- 速度慢
- csv驱动
- 架构不符合V5


archive目录：

仅保存历史参考。


# 9. 当前开发原则


不要：

- 为测试而修改架构
- 为GitHub清理改变项目设计
- 继续修复废弃代码


应该：

- 保持模块化
- 数据统一
- 增量开发
- 每个模块可独立验证


# 10. 新会话使用方式


开始新ChatGPT会话：

上传：

PROJECT_CONTEXT.md


并输入：

"这是我的A股量化项目，请阅读 PROJECT_CONTEXT.md，根据当前状态继续开发，不要改变整体架构。"

