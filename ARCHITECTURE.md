# Architecture

更新时间：2026-08-05


# V5 架构目标

建立统一的数据采集、存储、分析架构。


核心原则：

所有数据写入必须经过 Writer Layer。


---


# 当前架构


## 数据来源层


来源：

- AkShare
- Tushare
- BaoStock


负责：

获取原始数据。


---


## 数据处理层


负责：

- 数据清洗
- 类型转换
- 字段标准化


---


## Writer Layer（新增核心）


位置：

data/writer.py


职责：

统一数据库写入。


提供：

- insert_dataframe

批量 DataFrame 写入


- insert_ignore

替代：

INSERT OR IGNORE


- insert_replace

替代：

INSERT OR REPLACE


- execute_sql

执行复杂 SQL


---


# 重构前


脚本：

download_xxx.py


直接：

sqlite3.connect

cursor.execute

commit


问题：

- 重复代码大量存在
- 数据库逻辑分散
- 难维护


---


# 重构后


脚本：

download_xxx_v5.py


流程：


数据源

↓

DataFrame

↓

Writer

↓

Database



---


# 当前影响


已完成迁移：

- index
- industry
- dividend


待迁移：

- profit
- daily
- financial

