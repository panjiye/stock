# CURRENT_STATUS.md

# A股量化系统当前状态

更新时间： 2026-08-05

当前版本： V5-dev

------------------------------------------------------------------------

# 一、项目目标

本项目为 A 股量化研究系统。

核心流程：

数据采集 ↓ 数据库存储 ↓ 数据查询 ↓ 因子计算 ↓ 股票评分 ↓ 策略生成 ↓
回测分析 ↓ 风险控制

当前重点：

完成 V4.2 到 V5 数据访问层迁移。

------------------------------------------------------------------------

# 二、当前架构状态

当前正式架构：

scripts ↓ data.writer ↓ database ↓ analysis ↓ strategy ↓ backtest

数据库访问原则：

所有新的数据写入必须经过：

data/writer.py

禁止新代码：

-   直接 sqlite3.connect()
-   直接 cursor.execute()
-   直接 df.to_sql()

------------------------------------------------------------------------

# 三、已完成迁移

Writer Layer：

文件：

data/writer.py

状态：

完成。

支持：

-   dataframe写入
-   insert ignore
-   insert replace
-   upsert
-   SQL执行封装

已完成 V5 化脚本：

-   scripts/download_index.py
-   scripts/download_industry.py
-   scripts/download_dividend_all_v5.py
-   scripts/download_dividend_one_v5.py
-   scripts/download_one_stock_v5.py
-   scripts/download_daily_qfq_all_v5.py

------------------------------------------------------------------------

# 四、废弃路线

以下文件属于历史版本：

-   scripts/download_profit_all.py
-   scripts/download_financial_all_v2.py

用途：

仅作为历史参考。

禁止继续作为新开发入口。

------------------------------------------------------------------------

# 五、当前财务数据路线

正式入口：

scripts/download_financial_all_v5.py

流程：

数据源 ↓ financial tables ↓ financial_normalize.py ↓ financial_factor.py
↓ stock_score.py

------------------------------------------------------------------------

# 六、当前开发重点

Financial Data V5 完整性检查：

重点文件：

-   scripts/download_financial_all_v5.py
-   scripts/build_financial_normalized.py
-   analysis/financial_normalize.py
-   scripts/build_financial_factor.py
-   analysis/financial_factor.py

检查：

-   是否完全 writer 化
-   是否存在旧数据库调用
-   字段是否符合 DATABASE.md
-   财务表是否完整
-   下游因子计算是否正常

------------------------------------------------------------------------

# 七、开发原则

1.  不重新设计架构
2.  不推翻已有 V4.2 稳定逻辑
3.  不修改 archive 历史代码
4.  小步迁移
5.  保持数据库结构稳定

------------------------------------------------------------------------

# 八、重要文件

必须阅读：

-   PROJECT_CONTEXT.md
-   ARCHITECTURE.md
-   DATABASE.md
-   DEVELOPMENT_PLAN.md
-   V5_MIGRATION_PLAN.md
-   TODO.md

archive 目录仅用于历史参考，不代表当前开发状态。

# CURRENT_STATUS.md

# A股量化系统当前状态

更新时间： 2026-08-05

当前版本： V5-dev

------------------------------------------------------------------------

# 一、项目阶段

当前阶段：

## Factor Layer 开发与验证阶段

项目已完成：

V4.2 → V5 数据访问层迁移。

当前不再处理：

-   Writer Layer
-   Query Layer
-   Database V5结构
-   Financial Data V5迁移

以上模块已经完成并验证。

------------------------------------------------------------------------

# 二、当前系统架构

正式流程：

数据采集 ↓ V5数据库 ↓ data.query ↓ 因子计算 ↓ 股票评分 ↓ 策略生成 ↓
回测验证

------------------------------------------------------------------------

# 三、已完成模块

## 数据访问层 V5

状态：

完成。

包括：

-   data/writer.py
-   data/query.py
-   database结构

------------------------------------------------------------------------

## Financial Data V5

状态：

完成并验证。

正式入口：

scripts/download_financial_all_v5.py

相关流程：

financial tables ↓ financial_normalize.py ↓ financial_factor.py

------------------------------------------------------------------------

# 四、废弃路线

以下仅作为历史参考：

-   scripts/download_profit_all.py
-   scripts/download_financial_all_v2.py

archive目录：

仅保存历史代码。

不代表当前开发状态。

------------------------------------------------------------------------

# 五、当前开发重点

## Factor Layer

重点文件：

-   analysis/financial_normalize.py
-   analysis/financial_factor.py
-   analysis/valuation.py
-   analysis/technical.py
-   analysis/stock_score.py

目标：

-   确认因子输入统一
-   确认因子输出字段
-   完善因子计算链路
-   保持评分系统稳定

------------------------------------------------------------------------

# 六、下一阶段

Factor Layer完成后：

进入：

Strategy Layer

然后：

Backtest Validation

原则：

不重构已有V4.2回测框架。

------------------------------------------------------------------------

# 七、开发原则

1.  不重新设计架构
2.  不推翻已验证模块
3.  不修改archive历史代码
4.  小步修改
5.  保持数据库和接口兼容

------------------------------------------------------------------------

# 八、AI启动阅读顺序

新对话必须优先阅读：

-   PROJECT_CONTEXT.md
-   ARCHITECTURE.md
-   DATABASE.md
-   CURRENT_STATUS.md
-   TODO.md
-   V5_MIGRATION_PLAN.md

不要根据旧脚本判断当前任务。
# Factor Layer 状态

更新时间：
2026-08-05


当前状态：

Factor Layer Pipeline 已建立。


新增：

analysis/factor_pipeline.py


作用：

统一管理：

- financial factor
- valuation factor
- technical factor


当前流程：

financial_factor
        |
valuation
        |
technical
        |
        ↓
factor_pipeline
        |
        ↓
stock_score


下一阶段：

Strategy Layer 接入。

Factor Layer Pipeline 整合完成，准备进入 Strategy Layer