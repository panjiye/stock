# Stock Quant Project Context

## 项目名称

A股多因子量化研究系统


---

# 当前版本

Version:

v4.2 Research Prototype


状态:

冻结准备重构


---

# 项目定位

本项目是一个：

A股多因子选股 + 回测验证系统


目标：

通过：

- 行情数据
- 财务数据
- 技术指标
- 估值指标
- 因子评分

构建股票选择模型，并通过历史数据回测验证。


---

# 当前项目阶段

## 已完成

### 数据层

完成：

- 股票基础信息
- 行情数据
- 财务数据获取
- 财务数据标准化


### 因子层

已有：

- 财务因子
- 质量因子
- 估值因子
- 技术因子
- 综合评分


### 回测层

已有：

- 股票交易模拟
- 组合管理
- 交易成本
- 风险控制
- 回测报告


---

# 当前主要问题

## 1. 缺少统一运行入口

目前：

多个 scripts 和测试文件可以运行。

没有：

统一 pipeline。


---

## 2. 文件版本混乱

历史开发过程中：

存在：

engine.py

engine_v2.py

engine_v3.py

engine_v4_2.py


实际版本不能依靠文件名判断。


---

## 3. 研究代码和生产代码混合

当前：

scripts/

tests/

backtest/

存在大量历史实验文件。


---

# 当前真实核心模块


## 数据

scripts:

- download_daily_qfq_all.py
- download_financial_all_v2.py


## 因子

analysis:

- financial_factor.py
- financial_quality.py
- valuation.py
- technical.py
- stock_score.py


## 策略

strategy:

- scoring.py
- market_filter.py


## 回测

backtest:

- engine_v4_2.py
- portfolio.py
- trader.py
- broker.py
- risk_v2.py
- report_v4_2.py


---

# 当前真实运行链路


数据

↓

数据库

↓

因子计算

↓

股票池

↓

策略

↓

回测

↓

报告


---

# v5.0目标


不是增加更多策略。


目标：

工程化。


实现：

- 一个数据入口
- 一个因子入口
- 一个回测入口
- 一个报告入口


---

# 开发原则


以后：

禁止：

engine_v5.py

strategy_new.py


版本由：

Git Tag

管理。


代码文件保持稳定。


---

# 新会话启动说明


打开新的 ChatGPT 会话时：

上传：

- PROJECT_CONTEXT.md
- ARCHITECTURE.md
- TODO.md


并说明：

“基于当前 v4.2 状态继续 v5.0 重构，不重新设计架构。”