# Stock Project File Cleanup Plan


## 目标

整理 v4.2 项目。

原则：

不删除历史研究成果。

先 archive。

确认无价值后删除。


---

# KEEP 保留


## analysis


保留：


data/query.py
analysis/financial_factor.py
analysis/financial_quality.py
analysis/valuation.py
analysis/technical.py
analysis/stock_score.py



原因：

当前因子研究核心。


---

## strategy


保留：


strategy/scoring.py
strategy/market_filter.py



原因：

符合多因子方向。


---

## backtest


保留：


engine_v4_2.py

portfolio.py

trader.py

broker.py

cost.py

signal.py

performance.py

metrics.py

advanced_metrics.py

report_v4_2.py

risk_overlay_simulation.py

risk_stock_exit.py



---

# ARCHIVE


## backtest历史版本


移动：


engine.py
engine_v2.py
engine_v3.py

report_v1.py
report_v2.py

benchmark_v1.py

risk.py



目标：


archive/backtest/



---

## strategy历史版本


移动：


macd.py
ma_cross.py



目标：


archive/strategy/



---

## scripts历史版本


移动：


build_stock_pool_v1.py

download_daily.py

download_daily_raw_all.py

download_financial_all.py



目标：


archive/scripts/



---

# DELETE


确认后删除：


pycache

tests/t1.py

临时debug文件


---

# MOVE


## engine_v4_2.py


未来：


backtest/engine.py



原因：

版本由Git管理。


---

# 清理顺序


1.

建立 archive


2.

移动文件


3.

运行测试


4.

确认无引用


5.

删除垃圾文件