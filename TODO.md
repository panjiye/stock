# TODO

更新时间：2026-08-06
版本：V5.0-beta

## 当前优先级

当前阶段的目标是先完成一个可运行、可测试、可比较的 V5.0 Beta 基线，而不是先做 V5.1 技术因子重构。

## 已完成

- [x] Writer Layer 与 Query Layer 基础建设。
- [x] 财务数据 V5 下载入口与财报标准化链路。
- [x] 财务、估值、技术与综合因子评分。
- [x] Strategy Pipeline 基础接口。
- [x] Factor Backtest 接入 `select_strategy_stocks()`。
- [x] 历史回撤、行业、个股贡献及风险覆盖研究资产归档。
- [x] 清理空占位、缓存、扫描日志和重复 V4.1 结果副本。
- [x] V5.0 Beta 基线可信化：新增 coverage.csv，完整记录所有理论季度调仓（禁止静默跳过）。
- [x] V5.0 Beta 基线可信化：完善 params.json（回测截止日、调仓周期、手续费、滑点、因子版本、数据库版本、git commit）。
- [x] V5.0 Beta 基线可信化：升级 REPORT.md（数据覆盖说明、已知限制扩充、流程验证声明）。
- [x] 交易日匹配修复：新增 `get_nearest_price()`/`get_nearest_trade_price()`，按「当日或之前最近交易日」取买/卖价；EMPTY_CLOSE 由 28 → 0，回测期 56 → 84，equity 时间轴连续。


## V5.0 Beta 基线任务

### 1. 固化主链路

- [x] 确认 daily_price_qfq → financial_factor → valuation_factor → technical_factor → technical_quarter_factor → factor_score → strategy_pipeline → backtest_factor → results 的完整执行链路。
- [x] 处理当前阻塞运行的导入、路径、数据接口和脚本入口问题。
- [x] 确保脚本可直接运行并产出基础结果。

### 2. 生成标准结果输出

- [x] 在 results/v5/v5.0_baseline/ 下生成 equity.csv、trades.csv、holdings.csv、rebalance_records.csv。
- [x] 生成 coverage.csv，记录所有理论季度调仓的因子有无、股票数量、是否调仓及跳过原因，禁止静默跳过。
- [x] 生成 params.json、REPORT.md、charts/ 可视化输出。
- [x] 输出基础风险分析指标：CAGR、Sharpe、最大回撤、最大回撤周期、胜率、盈亏比、年度收益、月度收益。
- [x] 记录数据快照信息、git commit 信息和当前已知限制。

### 3. 形成统一运行入口

- [x] 确认 python -m scripts.backtest_factor 或 python -m scripts.run_v5_baseline 的可用性。
- [x] 让同一命令可重复生成 V5.0 Baseline。

### 4. 展示层 Dashboard

- [x] 生成浏览器可打开的仪表盘页面 [results/v5/v5.0_baseline/dashboard/index.html](results/v5/v5.0_baseline/dashboard/index.html)。
- [x] 将性能摘要、参数和结果文件入口集成到仪表盘中。

## 当前禁止项

- [ ] 不重构 technical.py。
- [ ] 不新增 v51 表。
- [ ] 不大规模拆分 analysis 模块。
- [ ] 不修改核心因子逻辑。
- [ ] 不优化未来函数问题。
- [ ] 不重设计数据库结构。

## 暂缓/延期

- [ ] V5.1：技术因子未来函数修复。
- [ ] V5.2：策略层完善。
- [ ] V5.3：风险层。
- [ ] V5.4：组合优化。

## 说明

在 V5.0 Baseline 未完成之前，不再推进 V5.1 的大规模因子重构和模块拆分。
