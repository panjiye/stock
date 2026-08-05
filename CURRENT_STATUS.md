# 当前项目状态

## V5 当前完成状态

更新时间：

2026-08

---

## 已完成

### Factor Layer

状态：

✅ 完成

包括：

* factor_score 数据
* 综合评分输出
* 因子排序

---

### Strategy Layer

状态：

✅ 完成

入口：

```
strategy/strategy_pipeline.py
```

功能：

* 因子结果接入
* 市场过滤
* MA/MACD 技术组合
* 输出标准交易信号

---

### Backtest Integration

状态：

✅ 完成

包括：

* strategy signal adapter
* factor backtest bridge

验证：

```bash
python -c "from strategy.strategy_pipeline import select_strategy_stocks"
```

通过。

---

## 当前进行中

### Risk Layer

目标：

* 回撤分析
* 回撤贡献分析
* 行业归因
* 风险暴露分析

---

## 下一阶段

建立：

```
Risk Layer
    |
    |
Performance Attribution
    |
    |
Portfolio Optimization
```
