"""
Strategy Layer 统一入口

版本:
V5-dev

职责:
1. 接收 Factor Layer 输出
2. 执行市场过滤
3. 组合技术信号
4. 输出标准策略信号
5. 提供组合选股接口
"""

from typing import Dict, List

from strategy.market_filter import check_market
from strategy.ma_cross import check_ma_cross
from strategy.macd import check_macd


def select_strategy_stocks(factor_df, top_n: int = 50) -> List[str]:
    """
    根据 Factor Layer 输出选择组合股票。

    输入:
        factor_df:
            包含 factor_score 字段的数据表
            需要至少包含:
            code
            final_score

    输出:
        股票代码列表

    设计原则:
        Strategy Layer 负责选股规则。
        不负责因子计算和交易执行。
    """

    if factor_df is None or len(factor_df) == 0:
        return []

    required = ["code", "final_score"]

    for col in required:
        if col not in factor_df.columns:
            raise ValueError(f"missing column: {col}")

    selected = (
        factor_df
        .sort_values(
            "final_score",
            ascending=False
        )
        .head(top_n)
    )

    return selected["code"].tolist()


def build_strategy_signal(
    code: str,
    factor_snapshot: Dict,
    price_df,
    require_market_filter: bool = True,
) -> Dict:

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

    signal = "BUY" if total_score >= 70 and technical_signal else "HOLD"

    return {
        "code": code,
        "signal": signal,
        "reason": reasons,
    }
