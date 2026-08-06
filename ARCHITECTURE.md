# 系统架构

更新时间：2026-08-06
版本：V5-dev

## 架构目标

建立面向 A 股多因子研究的模块化平台。V5 采用渐进迁移方式：保留历史研究代码与已有回测资产，通过数据访问层、因子层和策略适配层逐步统一新链路，不进行一次性重构。

## 当前数据流

```text
Baostock / EastMoney / Tushare
        ↓
下载脚本：日线、财报、指数、行业、分红
        ↓
SQLite：database/stock.db
        ↓
data.query / data.writer
        ↓
数据标准化与因子构建
  financial_profit → financial_profit_normalized → financial_factor
  daily_price_qfq → technical_factor → technical_quarter_factor
  财务因子 + 估值因子 + 季度技术因子 → factor_score
        ↓
Strategy Layer：按 final_score 选择组合
        ↓
Factor Backtest：scripts/backtest_factor.py
        ↓
标准化回测结果（待建设）→ Risk Layer → Portfolio Layer
```

## 数据与存储职责

| 层级 | 主要文件/表 | 职责 |
| --- | --- | --- |
| 数据下载 | `scripts/download_*` | 从外部数据源获取原始行情、财报、指数、行业、分红数据。 |
| 查询层 | `data/query.py` | 统一提供业务模块所需的只读数据查询。 |
| 写入层 | `data/writer.py` | 提供 DataFrame 插入、冲突忽略、upsert 和事务 SQL 执行。 |
| 核心数据库 | `database/stock.db` | 保存约 1,694 万条前复权行情、48.5 万条财报及综合因子等研究数据。 |
| 原始/标准化财报 | `financial_profit`、`financial_profit_normalized` | 原始层保留来源格式；标准化层统一百分比字段为小数。 |

## 因子层职责

- `analysis/financial_normalize.py`：处理财报百分比历史格式差异。
- `analysis/financial_factor.py`：计算 ROE、增长、稳定性和财务质量评分。
- `analysis/technical.py`：计算均线、动量、波动率和技术评分。
- `scripts/build_valuation_factor.py`：计算 PE、PE 分位与估值评分。
- `scripts/build_factor_score.py`：按财务 40%、估值 30%、技术 30% 生成 `factor_score`。
- `analysis/factor_pipeline.py`：提供统一因子快照的数据结构适配，不替代既有计算逻辑。

## 策略与回测职责

- `strategy/strategy_pipeline.py`：提供组合选股和标准策略信号接口。
- `scripts/backtest_factor.py`：当前 V5 可用回测主线；以公告日期过滤可用因子，季度调仓并选取 TOP50。
- `backtest/v5_strategy_adapter.py`：定义策略信号到回测信号的适配格式。
- `backtest/portfolio.py`、`broker.py`、`cost.py`：保留既有持仓、成交和交易成本模型。
- `archive/backtest/`、`archive/results/`：冻结的 V4.1/V4.2 回测、回撤归因、报告和风险覆盖研究资产，不属于当前运行主线。

## 当前运行边界

当前 V5 基准回测的真实闭环为：

```text
factor_score → strategy_pipeline.select_strategy_stocks()
→ scripts/backtest_factor.py → 根目录临时 CSV

冻结的当前基准已整理到 `results/v5/baseline/`。将脚本输出改为版本化目录属于后续 P1 工作，本次清理未修改 Python 代码。
```

`build_strategy_signal()` 的市场过滤、MA/MACD 信号，以及 `v5_strategy_adapter.py` 尚未进入该基准回测的执行路径。旧版通用 engine 与 V4.2 engine 已归档；当前不得把它们作为 V5 主入口。

## 架构规则

1. 新增业务查询应通过 `data.query`，新增写入应优先通过 `data.writer`。
2. 原始财报的百分比标准化只在 `analysis/financial_normalize.py` 处理；下载层不得重复转换。
3. 不重建、不清空现有 `database/stock.db`；真实数据库 schema 已比早期建表脚本更完整。
4. `archive/` 为历史研究代码，只做参考，不作为当前主线的修改对象。
5. 新的回测、风控与组合功能应建立在统一的 V5 结果输出之上。
