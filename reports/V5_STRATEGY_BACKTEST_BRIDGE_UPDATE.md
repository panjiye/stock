# V5 Strategy Layer → Factor Backtest 接入记录

版本：V5-dev

日期：2026-08-05

---

# 一、本次目标

将 V5 Strategy Layer 正式接入现有 Factor Backtest 流程。

目标：

将：

```
factor_score
    ↓
策略选择
    ↓
回测执行
```

形成统一链路。

---

# 二、架构原则

本次接入遵循：

* 不重构回测框架
* 不修改成熟交易执行模块
* 不改变数据库结构
* 不引入新的回测入口

保持：

```
backtest/engine_v4_2.py
backtest/portfolio.py
backtest/broker.py
backtest/risk_v2.py
```

稳定。

---

# 三、当前 V5 回测真实流程

调整后：

```
database

    ↓

factor_score

    ↓

scripts/backtest_factor.py

    ↓

strategy.strategy_pipeline

    ↓

股票组合选择

    ↓

portfolio

    ↓

performance report
```

---

# 四、代码修改

## 1. scripts/backtest_factor.py

增加：

```python
from strategy.strategy_pipeline import select_strategy_stocks
```

---

## 2. select_stocks() 修改

保留：

## 公告日期过滤

```python
available = factor[
    factor["pub_date"]
    <=
    rebalance_date
].copy()
```

原因：

避免未来函数。

---

保留：

```python
groupby("code").tail(1)
```

原因：

获取当前调仓日最新有效因子快照。

---

替换原有：

```python
available = (
    available
    .sort_values(
        "final_score",
        ascending=False
    )
)

result = (
    available
    .head(TOP_N)
    ["code"]
    .tolist()
)
```

改为：

```python
result = select_strategy_stocks(
    available,
    top_n=TOP_N
)
```

---

# 五、Strategy Layer职责调整

现在：

## Factor Layer

负责：

* 财务因子
* 估值因子
* 技术因子
* 综合评分

输出：

```
factor_score
```

---

## Strategy Layer

负责：

* 股票选择
* 市场过滤
* 技术确认
* 交易规则

---

## Backtest Layer

负责：

* 调仓执行
* 成交模拟
* 资金管理
* 收益统计

---

# 六、当前完整链路

```
factor_score

    ↓

strategy_pipeline.select_strategy_stocks()

    ↓

TOP50组合

    ↓

execute_sell()

    ↓

execute_buy()

    ↓

portfolio

    ↓

performance
```

---

# 七、验证

覆盖代码后运行：

```bash
python -c "from scripts.backtest_factor import select_stocks; print('backtest factor strategy bridge ok')"
```

预期：

```
backtest factor strategy bridge ok
```

---

# 八、Git提交

确认：

```bash
git status
```

然后：

```bash
git add \
scripts/backtest_factor.py \
strategy/strategy_pipeline.py \
BACKTEST_INTEGRATION_STATUS.md \
CURRENT_STATUS.md \
DEVELOPMENT_LOG.md \
TODO.md \
V5_STRATEGY_BACKTEST_BRIDGE_UPDATE.md
```

提交：

```bash
git commit -m "feat: connect v5 strategy layer with factor backtest"
```

推送：

```bash
git push origin v5-dev
```

---

# 九、下一阶段

完成本阶段后：

进入：

## V5 Pipeline Validation

目标：

首次运行完整链路：

```
Factor

↓

Strategy

↓

Backtest

↓

Report
```

重点验证：

* 是否正常生成交易记录
* 是否存在空仓异常
* 是否存在未来函数
* 收益曲线是否正常

暂不进行策略优化。
