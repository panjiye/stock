# Backtest Integration Status

版本：V5-dev
日期：2026-08-05

## 当前阶段

V5 Strategy Layer 与 Factor Backtest 接入。

## 当前真实链路

factor_score

↓

strategy_pipeline

↓

scripts/backtest_factor.py

↓

portfolio

↓

performance report

## 架构原则

保持稳定：

- backtest/engine_v4_2.py
- portfolio
- broker
- risk

不进行核心回测重构。

## 已完成

- Factor Layer
- Strategy Pipeline 基础结构
- Backtest Adapter 基础结构

## 当前任务

将 Strategy Layer 正式接管组合选股逻辑。
