# A股量化研究系统项目上下文

更新时间：2026-08-06
版本：V5-dev

## 当前定位

建立模块化A股量化研究平台。

当前主线：

数据层 → 因子层 → 策略层 → 回测 → 风险分析 → 组合管理

禁止重新设计架构，继续基于V5路线开发。

## 当前状态

已完成：

- Writer Layer
- Query Layer
- Database V5结构
- Financial Data V5
- Factor Layer
- Strategy Pipeline
- Backtest Integration

## 当前重点

Risk Layer建设：

- 回撤分析
- 回撤贡献分析
- 行业归因
- Benchmark分析

## 财务数据说明

旧：

scripts/download_profit_all.py

状态：废弃，仅历史参考。

当前入口：

scripts/download_financial_all_v5.py

流程：

EastMoney → financial_*表 → Factor Layer

## 开发原则

- 小步修改
- 保持兼容
- 不修改数据库设计
- 不影响archive历史代码
- 修改后同步文档
