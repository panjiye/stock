# A股量化研究系统项目上下文

更新时间：

2026-08-05


当前版本：

V5-dev


开发分支：

v5-dev


# 项目定位

建立完整 A 股量化研究平台：

数据获取

→ 数据库管理

→ 因子计算

→ 股票池

→ 策略

→ 回测

→ 报告


---

# 当前开发阶段

从 V4.2 Clean Baseline 迁移到 V5 架构。


# 已完成

## 数据层

完成：

- writer统一写入设计
- index迁移
- industry迁移
- dividend迁移


## 新增工具

- migrate_writer_v5.py
- migrate_dividend_writer_v5.py


# 当前重点

继续消除脚本中的：

sqlite3.connect

cursor.execute

INSERT OR IGNORE

INSERT OR REPLACE


统一进入：

data.writer


---

# 技术环境

Ubuntu Desktop 26.04 LTS

Python 3.14

数据库：

SQLite

database/stock.db


---

# 新会话使用方式

上传：

PROJECT_CONTEXT.md

并说明：

"这是我的A股量化项目，请根据当前V5状态继续开发，不改变整体架构。"
# PROJECT_CONTEXT.md

# A股量化选股系统项目上下文

更新时间：

2026-08-05

# 项目目标

开发一个个人使用的 A 股量化选股与回测系统。

目标：

* 自动获取 A 股历史数据
* 建立统一数据库
* 构建基本面 + 技术面因子
* 进行股票筛选
* 进行策略回测
* 分析收益、风险、回撤
* 逐步发展为 V5 架构

# 当前版本

当前基线：

V4.2 Clean

Git:

已建立：

v4.2-clean

当前开发分支：

v5-dev

# 当前状态

## 已完成

### 数据层

SQLite 数据库：

database/stock.db

已有主要表：

* daily_price_qfq
* daily_price_hfq
* daily_price_raw
* index_price
* daily_indicator
* technical_factor
* valuation_factor
* financial_factor
* financial_profit
* stock_basic
* stock_pool

### 行情来源

主要日线行情：

baostock

原因：

* 免费
* 稳定
* 历史数据完整

其他数据：

可能结合：

* AkShare
* Tushare
* 网络爬取

原则：

行情数据统一进入 SQLite。

不同来源数据需要标准化。

# 当前代码结构

```
analysis/

数据查询
指标计算


strategy/

策略逻辑


backtest/

回测


database/

数据库


archive/

历史废弃代码
```

# 已完成整理

完成：

* 清理旧回测文件
* 将废弃代码移动 archive
* 保留 V4.2 基线
* 建立 V5 开发分支

# 当前注意事项

不要：

修改 archive

不要：

继续优化旧 risk_stock_exit_v2

原因：

速度慢，设计方向需要废弃。

# 当前问题

pytest 已清理。

当前没有有效测试。

后续需要重新建立：

针对核心模块的小测试。

# V5方向

核心：

重新设计更清晰的数据流。

重点：

1. 数据标准化

2. 因子体系

3. 股票池

4. 评分模型

5. 策略

6. 风控

# AI 工作原则

任何开发：

先阅读：

PROJECT_CONTEXT.md

ARCHITECTURE.md

TODO.md

不要重新设计项目。
