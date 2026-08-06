# 项目状态

更新时间：2026-08-06
版本：V5-dev

## 当前定位

项目处于“V5 因子—策略—回测基础链路完成，进入基线可信化与 Risk Layer 建设”的阶段。当前主要用途是 A 股多因子研究和历史回测，不是实盘交易系统。

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
- 已建立 `results/v5/baseline/` 作为冻结基准位置；`scripts/backtest_factor.py` 当前仍会在根目录生成输出，尚未接入该标准目录。
- 参数快照、持仓/调仓记录与统一报告仍待补齐。

### P1：数据与 schema 一致性

- `scripts/create_tables.py` 与真实数据库 schema 存在差异，不可直接用于重建现有数据库。
- 财报下载脚本目前将 `gp_margin` 和 `np_margin` 映射为同一来源字段，需要核对来源字段语义。
- 股票池、季度技术因子等派生表需要建立明确的刷新顺序和刷新状态。

### P2：迁移收尾

- 部分脚本仍绕过 `data.writer` 直接写库。
- 历史报告/归因脚本已归档；Risk Layer 需要在当前架构中重新建立统一入口。

## 当前开发重点

先完成无未来数据泄漏的可信基线与标准化结果输出，再进入最大回撤、贡献归因、行业归因、基准比较等 Risk Layer 工作。
