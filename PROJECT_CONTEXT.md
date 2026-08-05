注意：archive目录中的脚本仅用于历史参考，不代表当前开发状态。当前开发状态必须以 CURRENT_STATUS.md、TODO.md 和 V5_MIGRATION_PLAN.md 为准。

# A股量化研究系统项目上下文

更新时间：

2026-08-05


当前版本：

V5开发阶段


开发分支：

v5-dev


# 当前重点

正在进行：

数据库访问层重构。


核心目标：

所有数据写入统一经过：

data.writer


所有查询统一经过：

data.query


# 已完成

## Writer层

完成：

- data/writer.py升级
- DataFrame批量写入
- upsert支持


## 已迁移脚本

- download_index.py
- download_industry.py
- dividend系列
- one_stock下载


## 新增工具

- migrate_writer_v5.py
- migrate_dividend_writer_v5.py


# 当前待处理

优先：

download_profit_all.py


然后：

download_daily_qfq_all.py

download_financial_all_v2.py


# 当前开发原则

不要：

- 修改废弃代码
- 破坏V4.2稳定版本
- 为清理而改变架构


应该：

- 小步迁移
- 每次迁移可运行验证
- 保持V5架构一致

# Project Context

更新时间：

2026-08-05


项目：

A股量化分析系统


分支：

v5-dev


---


# 当前阶段


数据库访问层重构阶段。


目标：

统一所有数据入口。


---


# 当前完成


完成：

## Writer Layer

状态：

完成。


## 指数下载

完成。


## 行业分类下载

完成。


## 分红数据下载

完成。


---


# 当前代码状态


稳定：

- data/writer.py
- download_index.py
- download_industry.py
- dividend v5 系列


测试：

通过。


---


# 未完成


## 财务数据迁移


涉及：

download_profit_all.py


download_financial_all_v2.py



## 日线数据迁移


涉及：

download_daily_qfq_all.py



---


# 开发原则


以后新增：

数据获取

↓

标准化 DataFrame

↓

Writer

↓

数据库



禁止：

脚本直接连接数据库。


---


# 最近 Git


重要提交：

5c68e57

migrate download_index to writer layer


691bdb2

migrate download_industry to writer upsert layer


3b1e210

add dataframe upsert writer


268df88

migrate dividend downloader to writer layer


9427bd0

add writer migration tools

