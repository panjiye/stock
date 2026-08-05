# A-stock Quant Architecture


## 当前架构


目前：


Data

↓

Scripts

↓

Analysis

↓

Strategy

↓

Backtest

↓

Results




存在问题：

数据、因子、策略耦合。


---

# v5目标架构



             main.py

                |

          Research Pipeline


                |

    |    |   |   |

        Data Factor Portfolio Risk

    |    |   |   |

        SQLite Matrix Holdings Metrics

                |

          Backtest Engine


                |

          Report Engine


---

# 模块说明


## Data


负责：

- 行情
- 财务
- 基础信息


禁止：

策略读取原始接口。



---

## Factor


负责：

生成：

stock-factor-date


例如：


000001

2025-01-01

ROE

PE

Momentum




---

## Strategy


负责：

根据因子生成：

买入卖出信号。



---

## Portfolio


负责：

仓位：

- 股票数量
- 权重
- 调仓



---

## Backtest


负责：

模拟真实交易。


必须支持：

- 手续费
- 滑点
- 涨跌停
- 停牌



---

## Risk


负责：

- 最大回撤
- 波动率
- beta
- 行业暴露
