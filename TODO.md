# TODO.md

更新时间：2026-08-05

当前版本：

V5-dev

------------------------------------------------------------------------

# 当前阶段

## 数据访问层 V5 迁移阶段

目标：

完成 V4.2 到 V5 数据访问层迁移。

原则：

-   保持数据库结构稳定
-   保持分析逻辑稳定
-   新代码统一经过 data.writer / data.query
-   不重新设计架构

------------------------------------------------------------------------

# 已完成任务

## Writer Layer

状态：完成

文件：

data/writer.py

支持：

-   DataFrame写入
-   insert_ignore
-   insert_replace
-   upsert
-   SQL封装

------------------------------------------------------------------------

## 已完成 V5 化脚本

-   download_index.py
-   download_industry.py
-   download_dividend_all_v5.py
-   download_dividend_one_v5.py
-   download_one_stock_v5.py
-   download_daily_qfq_all_v5.py

------------------------------------------------------------------------

# 废弃任务

## download_profit_all.py

状态：

废弃

说明：

旧财务下载流程，仅供历史参考。

当前正式入口：

scripts/download_financial_all_v5.py

## download_financial_all_v2.py

状态：

废弃

用途：

迁移参考。

------------------------------------------------------------------------

# 当前进行中

## Financial Data V5 完整性检查

检查：

-   download_financial_all_v5.py
-   build_financial_normalized.py
-   financial_normalize.py
-   build_financial_factor.py
-   financial_factor.py

任务：

-   检查 writer 使用情况
-   检查数据库调用
-   检查字段一致性
-   检查财务链路

------------------------------------------------------------------------

# 下一阶段

## Factor Layer

任务：

-   检查财务因子
-   检查技术因子
-   统一因子字段
-   增加因子质量检查

------------------------------------------------------------------------

## Strategy Layer

任务：

-   检查评分模型
-   检查因子权重
-   策略验证

------------------------------------------------------------------------

## Backtest Layer

原则：

V4.2 已稳定，不重构。

任务：

-   验证 V5 数据兼容
-   对比 V4.2 回测结果

------------------------------------------------------------------------

# AI协作规则

继续开发前必须阅读：

-   PROJECT_CONTEXT.md
-   ARCHITECTURE.md
-   DATABASE.md
-   V5_MIGRATION_PLAN.md
-   CURRENT_STATUS.md

不要根据 archive 或旧脚本判断当前任务。

# TODO.md

更新时间： 2026-08-05

当前版本：

V5-dev

------------------------------------------------------------------------

# 当前阶段

## Factor Layer 开发与验证

------------------------------------------------------------------------

# 已完成任务

## 数据访问层 V5

状态：

完成。

包括：

-   Writer Layer
-   Query Layer
-   Database结构

------------------------------------------------------------------------

## Financial Data V5

状态：

完成并验证。

正式入口：

scripts/download_financial_all_v5.py

------------------------------------------------------------------------

# 废弃任务

以下任务不再开发：

## download_profit_all.py

原因：

旧财务流程。

## download_financial_all_v2.py

原因：

V4迁移版本。

------------------------------------------------------------------------

# 当前任务

## 1. 因子链路检查

状态：

进行中。

检查：

-   financial_normalize.py
-   financial_factor.py
-   valuation.py
-   technical.py
-   stock_score.py

目标：

-   输入字段统一
-   输出字段稳定
-   因子计算完整

------------------------------------------------------------------------

# 2. Strategy Layer

待开始。

涉及：

strategy/

任务：

-   检查评分逻辑
-   检查市场过滤
-   验证策略输入

------------------------------------------------------------------------

# 3. Backtest Validation

待开始。

原则：

保持V4.2回测框架。

任务：

-   使用V5数据验证
-   对比历史结果
-   分析差异

------------------------------------------------------------------------

# AI协作规则

继续开发前必须阅读：

-   PROJECT_CONTEXT.md
-   ARCHITECTURE.md
-   DATABASE.md
-   CURRENT_STATUS.md
-   TODO.md
-   V5_MIGRATION_PLAN.md

不要重复检查已完成模块。

## Factor Pipeline

状态：

已完成第一阶段。


完成：

- 建立统一入口
- 统一因子输出结构
- 保留旧评分兼容


下一步：

- Strategy Layer 接入
- 回测验证