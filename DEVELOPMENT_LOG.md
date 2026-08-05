# 2026-08-05 Factor Layer Pipeline

完成：

新增：

analysis/factor_pipeline.py


目的：

建立V5 Factor Layer统一入口。


调整：

原：

financial_factor
valuation
technical

分别调用。


现：

financial_factor
valuation
technical

        ↓

factor_pipeline

        ↓

stock_score


原则：

- 不改变已有因子计算
- 不修改数据库
- 保持兼容
- 小步迁移