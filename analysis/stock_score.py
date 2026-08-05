"""
股票综合评分入口

当前状态：
V5 Factor Layer 迁移中。

兼容策略：
- 保留旧 fundamental_score 作为兼容入口
- 支持接入 financial_factor / valuation 等新因子结果
"""

from analysis.fundamental import fundamental_score


def combine_score(
    technical,
    financial,
    valuation=None
):
    """
    综合评分。

    当前默认保持旧逻辑兼容。
    新因子接入时支持：
    technical + financial + valuation
    """

    if valuation is None:
        return round(
            technical * 0.5
            + financial * 0.5,
            2
        )

    return round(
        technical * 0.4
        + financial * 0.4
        + valuation * 0.2,
        2
    )



def score_stock(
    code,
    technical_score,
    financial_factor=None,
    valuation_score=None
):
    """
    股票评分入口。

    参数：
        code
        technical_score
        financial_factor: V5财务因子结果（可选）
        valuation_score: 估值因子结果（可选）

    未传入新因子时保持V4.2兼容逻辑。
    """

    if financial_factor is None:
        fundamental = fundamental_score(code)
        fund_score = fundamental["score"]
        detail = fundamental["detail"]

    else:
        fund_score = financial_factor.get(
            "quality_score",
            0
        )
        detail = financial_factor


    total = combine_score(
        technical_score,
        fund_score,
        valuation_score
    )

    result = {
        "code": code,
        "technical_score": technical_score,
        "fundamental_score": fund_score,
        "total_score": total,
        "fundamental_detail": detail
    }

    if valuation_score is not None:
        result["valuation_score"] = valuation_score

    return result
