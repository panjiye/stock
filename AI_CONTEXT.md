AI 项目上下文记录

项目版本

v5-dev

原则：

不重新设计架构，不改变已有路线。

开发环境

项目：

~/python_projects/stock

下载目录：

~/下载

运行：

优先使用：

python -m scripts.xxx

开发要求：

大文件直接提供下载

测试先限制数量

修改提供完整替换文件
# AI_CONTEXT

更新时间:
2026-08-05

## 当前版本

v5-dev


## 财报数据链路

EastMoney
    |
download_financial_all_v5.py
    |
financial_profit
    |
build_financial_normalized.py
    |
analysis/financial_normalize.py
    |
financial_profit_normalized
    |
financial_factor


## 数据规则

financial_profit:
- 保存东方财富原始数据
- 下载层禁止处理百分比


financial_normalize:
- 统一百分比格式
- 处理东方财富历史字段:
  - 0.344620
  - 10.57

统一为小数。


## 已完成 Writer Layer

已迁移:
- index
- industry
- dividend


## 当前任务

财报下载迁移:

archive/scripts/download_financial_all.py

迁移到:

scripts/download_financial_all_v5.py


原则:
- 不改变数据源
- 不改变分析逻辑
- 只替换数据库访问层

## Financial data normalization


EastMoney download layer:

职责:
- 获取财报数据
- 字段映射
- 写入 financial_profit


financial_profit:

保存来源数据格式。
不同历史接口可能存在比例格式差异。


标准化位置:

analysis/financial_normalize.py


处理:

roe_avg
np_margin
gp_margin


规则:

如果:
value > 2

认为是百分比形式:

10.57

转换:

0.1057


否则:

保持:

0.34462


禁止:

download层重复除100。

## Financial data normalization


EastMoney download layer:

职责:
- 获取财报数据
- 字段映射
- 写入 financial_profit


financial_profit:

保存来源数据格式。
不同历史接口可能存在比例格式差异。


标准化位置:

analysis/financial_normalize.py


处理:

roe_avg
np_margin
gp_margin


规则:

如果:
value > 2

认为是百分比形式:

10.57

转换:

0.1057


否则:

保持:

0.34462


禁止:

download层重复除100。


##数据库访问规则

新代码统一使用：

data/writer.py

禁止直接新增：

sqlite3.connect()

独立 df.to_sql()

优先：

insert_dataframe()

insert_ignore()

upsert_dataframe()

execute_sql()

##财报模块

核心数据：

financial_profit

来源：

东方财富 EastMoney。

相关文件：

scripts/download_financial_all_v2.py

archive/scripts/download_financial_all.py

analysis/financial_normalize.py

analysis/financial_factor.py

analysis/fundamental.py

生成财报代码前必须检查：

数据来源

字段映射

标准化逻辑

下游依赖