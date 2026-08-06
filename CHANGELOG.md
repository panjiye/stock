# CHANGELOG

## 2026-08-06：V5.0 Beta 基线可信化

### 变更

- 在 [scripts/backtest_factor.py](scripts/backtest_factor.py) 中新增 coverage 输出：完整记录所有理论季度调仓期（有无 factor_score、股票数量、是否实际调仓、跳过原因），**禁止静默跳过**缺失季度。
- 完善 [params.json](results/v5/v5.0_baseline/params.json)：新增回测截止日、因子数据起始日、调仓周期、手续费率、滑点、因子版本、数据库版本与 git commit。
- 升级 [REPORT.md](results/v5/v5.0_baseline/REPORT.md)：新增数据覆盖说明、扩充已知限制，并明确"当前回测结果仅用于流程验证，不构成策略有效性结论"。
- Dashboard 增加 coverage 概要（理论期/实际调仓/跳过）。

### 影响

- 数据缺口从"静默丢失"变为"显式可见"：coverage.csv 揭示 85 个理论季度中 56 期实际调仓、29 期被跳过（28 期 EMPTY_CLOSE、1 期 EMPTY_STOCKS）。
- `pytest` 2 passed；完整 baseline 重新运行成功，资产仍为 15,389,833.64、56 笔交易，验证策略逻辑未改变。
- 未修改技术因子逻辑、未重构架构、未修改数据库。

## 2026-08-06：V5.0 Beta 基线首次落地

### 变更

- 将当前 V5 主回测入口接入标准结果输出目录 [results/v5/v5.0_baseline](results/v5/v5.0_baseline)。
- 增加持仓、调仓记录、参数快照、研究报告与基础图表输出。
- 新增统一入口 [scripts/run_v5_baseline.py](scripts/run_v5_baseline.py)。
- 增加最小 Web Dashboard 页面 [results/v5/v5.0_baseline/dashboard/index.html](results/v5/v5.0_baseline/dashboard/index.html)，用于浏览器中展示基线摘要。
- 生成第一版 V5.0 Beta 可交付基线产物。

### 影响

- 现在可直接从 [scripts/backtest_factor.py](scripts/backtest_factor.py) 或 [scripts/run_v5_baseline.py](scripts/run_v5_baseline.py) 产出标准基线文件。
- 当前基线已覆盖 equity、trades、holdings、rebalance_records、params.json、REPORT.md 和 charts/。

## 2026-08-06：项目瘦身与结构整理

### 变更

- 将项目当前优先级调整为“先完成 V5.0 Beta Baseline，再推进 V5.1 技术因子修复”。
- 暂停 V5.1 架构升级、v51 表新增和大规模模块拆分。
- 将后续工作重心收敛到“固化主链路、修复运行问题、生成可运行、可展示、可复盘的研究基线”。
- V5.0 Beta 交付标准从“生成 CSV”扩展为“包含回测结果、参数记录、研究报告、可视化与基础风险分析”。
- 当前阶段明确禁止重构 technical.py、修改核心因子逻辑、优化未来函数问题和重设计数据库结构。

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
