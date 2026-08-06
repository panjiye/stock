# 项目状态

更新时间：2026-08-06
版本：V5.0-beta

## 当前定位

项目当前优先级调整为“先完成 V5.0 Beta 基线，再进入 V5.1 技术因子修复、V5.2 策略完善、V5.3 风险层和 V5.4 组合优化”。当前目标不是追求完美架构，而是形成一个可运行、可测试、可比较的完整闭环。

## 当前阶段目标

### 已完成的第一轮 V5.0 Beta 基线

已完成以下落地工作：
- 以 [scripts/backtest_factor.py](scripts/backtest_factor.py) 为当前主回测入口，已成功产出标准结果目录 [results/v5/v5.0_baseline](results/v5/v5.0_baseline)。
- 已补齐回测输出文件：equity.csv、trades.csv、holdings.csv、rebalance_records.csv、params.json、REPORT.md 和 charts/。
- 已生成资金曲线、回撤曲线、年度收益、月收益热力图和换手率图。
- 已增加统一入口 [scripts/run_v5_baseline.py](scripts/run_v5_baseline.py)。
- 已补充最小 Web Dashboard 页面 [results/v5/v5.0_baseline/dashboard/index.html](results/v5/v5.0_baseline/dashboard/index.html)，可直接在浏览器中打开查看基线摘要和结果文件入口。

### 已完成的 V5.0 Beta 可信化阶段

在不修改技术因子逻辑、不重构架构、不修改数据库的前提下，对齐基线"可复现声明"与"数据缺口透明化"：
- 新增 [coverage.csv](results/v5/v5.0_baseline/coverage.csv)，完整记录全部 85 个理论季度调仓期（有无 factor_score、股票数量、是否实际调仓、跳过原因），**不再静默跳过**缺失季度。
- 完善 [params.json](results/v5/v5.0_baseline/params.json)，补齐回测截止日、调仓周期、手续费率、滑点、因子版本、数据库版本与 git commit。
- 升级 [REPORT.md](results/v5/v5.0_baseline/REPORT.md)，新增数据覆盖说明、扩充已知限制，并明确"当前回测结果仅用于流程验证，不构成策略有效性结论"。
- 运行校验：`pytest` 2 passed；完整 baseline 重新运行成功，资产仍为 15,389,833.64、56 笔交易，验证策略逻辑未改变。

### 已完成的交易日匹配修复（本轮）

针对 coverage.csv 揭示的 28 期 EMPTY_CLOSE 根因（卖出日/调仓日非交易日时精确日期匹配 daily_price_qfq 落空），在不改因子/策略/数据库的前提下修复价格获取逻辑：
- 新增 `get_nearest_price()`（批量）与 `get_nearest_trade_price()`（单股票）函数，统一按「target_date 当日或之前最近一个交易日」取价。
- 替换原买入 `get_open_price()` 与卖出 `get_close_price()` 的精确日期查询，复用最近交易日逻辑。
- 效果：EMPTY_CLOSE 由 28 → **0**；回测期由 56 → 84；equity 季度时间轴恢复连续（90~92 天均匀间隔，无缺口）。仅剩边界期 EMPTY_STOCKS（回测起点 2005-03-31 无可用因子）。

### 当前已验证结果（修复后）
- 回测最终资产：17,785,136.46
- 总收益：1678.51%
- 年化收益：14.87%
- 最大回撤：-61.04%
- Sharpe：0.5343
- 数据覆盖：85 个理论季度调仓期，84 期实际调仓（OK），1 期跳过（EMPTY_STOCKS，回测起点边界）。

### 1. 固化 V5.0 链路

确认并跑通以下链路：

daily data → financial factor → valuation factor → technical factor → technical_quarter_factor → factor score → strategy pipeline → backtest_factor → results

### 2. 修复运行问题

仅处理以下问题：

- 导入错误
- 路径错误
- 数据接口错误
- 脚本无法运行的问题

不提前优化设计，不重构核心因子计算逻辑，不修改数据库结构。

### 3. 生成第一个 V5.0 Baseline

目标输出目录为 results/v5/v5.0_baseline/，交付内容不仅是基础结果文件，而是一个完整可分析的量化研究基线，包含：

#### 3.1 回测核心结果

- equity.csv
- trades.csv
- holdings.csv
- rebalance_records.csv
- coverage.csv（逐期记录所有理论季度调仓：因子有无、股票数量、是否调仓、跳过原因）

用于后续复盘和二次分析。

#### 3.2 回测参数与环境记录

- params.json
  - 初始资金
  - 调仓周期
  - 股票数量 TOPN
  - 手续费
  - 滑点
  - 回测起止日期
  - 因子版本
  - 数据库版本
  - git commit

#### 3.3 研究报告

- REPORT.md
  - 策略说明
  - 因子说明
  - 回测周期
  - 收益指标
  - 风险指标
  - 当前已知限制

#### 3.4 可视化输出

- charts/
  - equity_curve.png
  - drawdown_curve.png
  - annual_return.png
  - monthly_return_heatmap.png
  - turnover.png
  - holdings_distribution.png（如当前数据支持）

#### 3.5 基础风险分析输出

- 基础指标包括：
  - CAGR
  - Sharpe
  - 最大回撤
  - 最大回撤周期
  - 胜率
  - 盈亏比
  - 年度收益
  - 月度收益

目标是让别人拿到 results/v5/v5.0_baseline/ 时，不看代码也能理解策略表现。

### 4. 形成可重复运行入口

目标是提供一个统一入口，例如：

- python -m scripts.backtest_factor
- 或 python -m scripts.run_v5_baseline

能够重新生成同样结果。

## 当前不做

- 暂停 V5.1 架构升级和技术因子重构。
- 不新增 v51 数据表。
- 不进行大规模模块拆分。
- 不修改当前核心因子计算逻辑。

## 已完成模块

### 数据层

- [x] SQLite 主库：`database/stock.db`。
- [x] Query Layer：`data/query.py`。
- [x] Writer Layer：`data/writer.py`。
- [x] 前复权日线、指数、行业、分红、财报下载脚本。
- [x] EastMoney 财报 V5 入口：`scripts/download_financial_all_v5.py`。
- [x] 财报原始数据到标准化数据的转换链路。

### 因子层

- [x] 财务质量、增长、稳定性因子。
- [x] 估值因子：PE 与 PE 分位。
- [x] 技术因子：均线、动量、波动率。
- [x] 季度技术因子与综合因子评分 `factor_score`。
- [x] 因子快照适配接口。

### 策略与回测

- [x] 基于 `final_score` 的组合选股接口。
- [x] 公告日可用性过滤。
- [x] TOP50、季度调仓的因子回测入口：`scripts/backtest_factor.py`。
- [x] 交易成本、Broker、Portfolio 等历史回测基础模块。
- [x] 策略信号到回测信号的适配接口。

### 历史研究与分析资产

- [x] V4.1/V4.2 回撤、归因、报告和风险覆盖研究代码及结果已归档至 `archive/`。
- [x] 历史下载、迁移和研究脚本已从当前 `scripts/` 主入口移出。
- [x] V5 基准回测产物已整理至 `results/v5/baseline/`：56 个季度周期，2005-09-30 至 2026-06-30，最终资产约 1,538.98 万元。

### 项目结构整理

- [x] 删除空占位数据库、空脚本、失效 `main.py`、缓存、扫描日志和过期目录清单。
- [x] 删除 9 个与 `results/baseline/v4.1/` checksum 完全一致的结果副本。
- [x] 将 `results/`、`results_v4_2/`、`results_risk_overlay/`、`backtest_result/` 归档至 `archive/results/`。
- [x] 保留 `database/stock.db`、`.venv/` 和项目快照包，未触碰核心数据与本地运行环境。

## 已核验数据状态

- `daily_price_qfq`：16,945,006 条，覆盖至 2026-08-05。
- `financial_profit`：485,334 条，财务报告期覆盖至 2026-06-30。
- `factor_score`：485,221 条。
- `technical_factor`：16,942,663 条。
- `technical_quarter_factor`：285,305 条。
- `stock_pool`：11,001 条，但最新股票池日期为 2026-03-31，未与最新因子完全同步。

## 当前问题

### P0：回测基线可信度

- 技术动量分位在完整历史序列上计算，历史时点可能使用未来数据；该问题会污染 `technical_quarter_factor`、`factor_score` 和 V5 基准回测。
- 因此当前基准收益、回撤、Sharpe 只能作为待复核的研究结果，不能直接作为策略有效性结论。

### P1：主线接口和结果不统一

- 当前可运行 V5 主线只使用 `select_strategy_stocks()` 的 TOP50 排序；市场过滤、MA/MACD 信号和策略适配器尚未接入基准回测。
- 失效的 V4.1/V4.2 engine、报告和归因入口已归档；如需复用，必须先以归档代码为参考建立新的 V5 实现。
- `scripts/backtest_factor.py` 已接入标准结果目录 [results/v5/v5.0_baseline](results/v5/v5.0_baseline)；参数快照、持仓/调仓记录与统一报告已补齐，并新增 coverage.csv 逐期数据覆盖记录。

### P1：回测时间轴连续性（已修复）

- 已修复：`get_nearest_price()` / `get_nearest_trade_price()` 按「target_date 当日或之前最近交易日」匹配，EMPTY_CLOSE 由 28 → 0，回测期由 56 → 84，equity 时间轴恢复连续。
- 当前仅剩边界期 EMPTY_STOCKS（回测起点 2005-03-31 无可用因子），属正常边界情形，非交易日匹配问题。

### P1：数据与 schema 一致性

- `scripts/create_tables.py` 与真实数据库 schema 存在差异，不可直接用于重建现有数据库。
- 财报下载脚本目前将 `gp_margin` 和 `np_margin` 映射为同一来源字段，需要核对来源字段语义。
- 股票池、季度技术因子等派生表需要建立明确的刷新顺序和刷新状态。

### P2：迁移收尾

- 部分脚本仍绕过 `data.writer` 直接写库。
- 历史报告/归因脚本已归档；Risk Layer 需要在当前架构中重新建立统一入口。

## 当前开发重点

先完成无未来数据泄漏的可信基线与标准化结果输出，再进入最大回撤、贡献归因、行业归因、基准比较等 Risk Layer 工作。
