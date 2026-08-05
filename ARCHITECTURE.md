# 系统架构


## 总体流程


数据源

↓

Downloader

↓

SQLite数据库

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



# 模块说明


## downloader

负责：

- baostock行情下载
- 财务数据获取


## database

存储：

统一数据。



## analysis

数据查询和基础计算。


## factor

因子计算。


未来建立。


## strategy

策略逻辑。


包括：

- 市场过滤
- 评分
- 买卖规则


## backtest

历史模拟。


包括：

- 回测引擎
- 风控
- 收益分析


## report

生成：

- 收益曲线
- 回撤
- 分析报告



# 设计原则


低耦合。

数据层和策略层分离。

所有策略必须可以历史验证。

