# CHANGELOG

## 2026-08-06：项目瘦身与结构整理

### 归档

- 将已被 V5 替代的旧下载、旧因子评分、旧迁移和历史研究脚本移至 `archive/scripts/` 与 `archive/tools/`。
- 将 V4.1/V4.2 回测、报告、回撤归因、风险覆盖代码移至 `archive/backtest/`。
- 将 `results/`、`results_v4_2/`、`results_risk_overlay/`、`backtest_result/` 归档至 `archive/results/`。
- 将当前 V5 基准输出整理至 `results/v5/baseline/`；将根目录其他历史实验输出归档。
- 将非项目运行说明文档移至 `archive/docs/`。

### 删除

- 删除空占位数据库、空脚本、失效的根目录 `main.py`。
- 删除缓存目录、扫描日志、过期目录/文件清单。
- 删除与 `results/baseline/v4.1/` 内容完全相同的 9 个重复结果文件。
- 删除重复状态文档：`AI_SESSION_CONTEXT.md`、`CURRENT_STATUS.md`、`DEVELOPMENT_PLAN.md`、`V5_MIGRATION_PLAN.md`。

### 保留

- 保留 `database/stock.db`、`.venv/`、`stock_quant_project_clean.tar.gz`。
- 保留当前 V5 数据、因子、策略与 `scripts/backtest_factor.py` 主链路。
- 保留项目状态、架构、决策、待办和数据库文档作为当前 AI 上下文。

### 影响

- 当前主目录只保留 V5 运行代码与核心文档，历史资产从主线中隔离。
- 历史回测工具和结果不再是可直接执行的当前入口；需要时应从 `archive/` 参考并重新接入 V5 架构。
- 未修改任何数据表、因子计算逻辑或 V5 主线 Python 代码内容。
