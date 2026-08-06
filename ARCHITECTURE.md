# Architecture

更新时间：2026-08-06

## V5架构

数据源
↓
数据处理
↓
Writer/Query Layer
↓
Factor Layer
↓
Strategy Layer
↓
Backtest
↓
Risk Layer
↓
Portfolio

## 核心规则

所有数据库写入必须经过：

data.writer

所有查询必须经过：

data.query

禁止：

- sqlite3直接写入
- 分散数据库逻辑
- 推翻V5结构

## 模块职责

Factor Layer：因子计算

Strategy Layer：信号组合

Backtest：执行验证

Risk Layer：风险分析
