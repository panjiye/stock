# Strategy Layer 状态

更新时间：
2026-08-05

当前版本：
V5-dev

---

# 当前阶段

Strategy Layer 接入阶段。

---

# 当前结构

```
Factor Layer
      ↓
stock_score
      ↓
strategy_pipeline
      ↓
Backtest
```

---

# 已存在模块

## scoring.py

职责：

技术指标综合评分。

包含：

- RSI
- MA趋势
- MACD
- KDJ


## market_filter.py

职责：

市场环境过滤。


## ma_cross.py

职责：

MA金叉信号。


## macd.py

职责：

MACD多头信号。

---

# 新增

## strategy_pipeline.py

作用：

作为 Factor Layer 和 Backtest 之间的桥梁。

负责：

- 接收因子结果
- 市场过滤
- 技术信号组合
- 输出标准交易信号

不负责：

- 因子计算
- 数据下载
- 回测执行

---

# 下一阶段

1. Strategy Pipeline 与 backtest signal 对接
2. 回测验证
3. 策略参数优化
