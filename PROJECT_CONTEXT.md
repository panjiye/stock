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
- 项目结构整理：当前 V5 主线、历史资产与临时产物已分离

## 当前重点

Risk Layer建设：

- 回撤分析
- 回撤贡献分析
- 行业归因
- Benchmark分析

## 财务数据说明

旧财务下载脚本已归档：

archive/scripts/legacy/download_profit_all.py

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

## 目录约定

- 当前可运行代码保留在 `analysis/`、`data/`、`strategy/`、`backtest/`、`scripts/`。
- 历史代码、回测结果和旧文档统一放在 `archive/`，不作为当前入口修改。
- V5 目标结果结构为 `results/v5/<版本>/`；当前冻结基准位于 `results/v5/baseline/`。现有回测脚本仍会写入根目录，后续应在标准化输出任务中迁移，清理阶段不改动其代码。
