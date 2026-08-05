"""
Strategy Layer 统一入口

版本:
V5-dev

职责:
1. 接收 Factor Layer 输出
2. 执行市场过滤
3. 组合技术信号
4. 输出标准策略信号

设计原则:
- 不修改已有策略组件
- 不负责因子计算
- 不负责回测执行
- 作为 Factor Layer 与 Backtest 的桥梁
"""

from typing import Dict, Optional

from strategy.market_filter import check_market
from strategy.ma_cross import check_ma_cross
from strategy.macd import check_macd


def build_strategy_signal(
    code: str,
    factor_snapshot: Dict,
    price_df,
    require_market_filter: bool = True,
) -> Dict:
    """
    根据因子快照和技术数据生成策略信号。

    返回:
    {
        code,
        signal,
        reason
    }
    """

    reasons = []

    if require_market_filter:
        if not check_market(price_df):
            return {
                "code": code,
                "signal": "HOLD",
                "reason": ["市场环境不满足交易条件"],
            }
        reasons.append("市场环境通过")

    financial = factor_snapshot.get("financial", {})
    valuation = factor_snapshot.get("valuation", {})
    technical = factor_snapshot.get("technical", {})

    total_score = factor_snapshot.get("total_score", 0)

    if financial:
        reasons.append("已接入财务因子")

    if valuation:
        reasons.append("已接入估值因子")

    technical_signal = False

    if check_ma_cross(price_df):
        reasons.append("MA金叉")
        technical_signal = True

    if check_macd(price_df):
        reasons.append("MACD多头")
        technical_signal = True

    if total_score >= 70 and technical_signal:
        signal = "BUY"
    else:
        signal = "HOLD"

    return {
        "code": code,
        "signal": signal,
        "reason": reasons,
    }
