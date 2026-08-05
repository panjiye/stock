# 系统架构

更新时间：

2026-08-05


# V5 架构目标

数据获取

↓

Downloader

↓

data.writer

↓

SQLite数据库

↓

data.query

↓

Analysis

↓

Factor

↓

Strategy

↓

Backtest

↓

Report


---

# 当前架构变化

V5 开始统一数据访问层。


## 写入层

新增：

data.writer


负责：

- dataframe写入
- insert ignore
- replace/upsert


原则：

业务脚本禁止直接 sqlite 写入。


## 查询层

data.query

负责：

数据库读取。


---

# 模块说明

## scripts

负责：

数据获取和转换。


不负责：

数据库细节。


## data

负责：

数据库访问。


包括：

query.py

writer.py


## analysis

数据分析。


## factor

因子计算。


## strategy

策略逻辑。


## backtest

历史验证。


---

# 设计原则

低耦合。

数据层和策略层分离。

所有策略必须历史验证。

所有数据写入统一入口。
