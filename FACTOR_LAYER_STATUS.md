# FACTOR_LAYER_STATUS.md

更新时间：
2026-08-05

版本：

V5-dev


# Factor Layer 当前状态


## 当前阶段

Factor Layer 整合阶段。


已经完成：

- V5 数据层
- Financial Data V5
- stock_score V5兼容接口


当前目标：

建立统一因子入口。


---

# 当前结构


financial_factor.py

        |

valuation.py ---- factor_pipeline.py ---- stock_score.py

        |

technical.py


---

# 新增模块


## analysis/factor_pipeline.py


职责：

统一管理：

- 财务因子
- 估值因子
- 技术因子


不负责：

- 策略逻辑
- 权重调整
- 买卖规则


---

# 设计原则

1. 保留已有因子模块

2. 不修改数据库结构

3. 不影响V4.2回测逻辑

4. 使用适配层逐步迁移


---

# 下一阶段

Strategy Layer 接入。

随后：

Backtest Validation
