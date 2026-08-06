# Database

更新时间：2026-08-06

数据库：
database/stock.db

类型：SQLite

## 数据访问规范

统一：

data.writer
data.query

禁止：

sqlite3.connect()
cursor.execute()
直接INSERT

## 财务数据

### financial_profit

状态：历史兼容表。

来源：旧profit下载流程。

当前不作为新开发入口。

### 当前财务入口

scripts/download_financial_all_v5.py

流程：

EastMoney
↓
financial_*表
↓
Factor Layer

新增财务因子优先使用新版financial数据。
