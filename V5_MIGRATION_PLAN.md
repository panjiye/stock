# Stock V5 Migration Plan


## 目标版本

v5.0


---

# 总体目标


将：

v4.2 Research Prototype


升级为：

模块化量化研究框架。


---

# Phase 0

## 冻结 v4.2


操作：

创建：

Git Tag


v4.2-final



目的：

保留历史状态。


---

# Phase 1

## 项目整理


建立：


archive/



移动：

历史版本代码。


不修改逻辑。


---

# Phase 2

## 建立 v5目录结构


目标：


stock/

data/

factors/

universe/

strategy/

portfolio/

backtest/

risk/

report/

pipeline/

archive/



---

# Phase 3

## 数据层迁移


当前：


data/query.py



迁移：


data/



目标：

统一数据访问。


---

# Phase 4

## 因子层迁移


当前：


analysis/



迁移：


factors/



结构：


factors/

fundamental.py

quality.py

value.py

technical.py

scoring.py



---

# Phase 5

## 回测迁移


当前：


engine_v4_2.py



调整：


engine.py



同时：

保持：

portfolio

trader

risk


---

# Phase 6

## 建立Pipeline


新增：


pipeline/

run_data.py

run_factor.py

run_backtest.py

run_report.py

run_all.py



最终：

运行：


python -m pipeline.run_all



---

# Phase 7

## 删除历史代码


条件：

- 无import引用
- 无运行依赖
- Git已有保存


---

# v5完成标准


## 工程

✅ 单入口

✅ 可重复运行


## 数据

✅ 数据流程明确


## 因子

✅ 因子统一接口


## 回测

✅ 策略和交易分离


## 报告

✅ 自动生成


---

# 注意事项


禁止：

一次性重写。


采用：

小步迁移。


每完成一个阶段：

Git commit。