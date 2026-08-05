# Backtest Integration 状态

更新时间：2026-08-05

版本：V5-dev

---

## 当前阶段

Backtest Integration

目标：

将 V5 Factor Layer 与 Strategy Layer 接入现有 V4.2 回测框架。

---

## 当前架构

```text
Factor Pipeline
        ↓
Strategy Pipeline
        ↓
V5 Strategy Adapter
        ↓
Backtest Engine V4.2
        ↓
Portfolio / Broker
```

---

## 已完成

新增：

`backtest/v5_strategy_adapter.py`

职责：

- 转换 Strategy Layer 输出
- 保持 engine_v4_2 不修改
- 保持旧回测兼容

---

## 设计原则

不修改：

- engine_v4_2.py
- portfolio.py
- broker.py
- risk模块

仅增加适配层。

---

## 下一步

1. 编写 V5 Pipeline 回测测试
2. 验证 signal → trader → engine 链路
3. 运行首次 V5 回测
