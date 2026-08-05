"""
Factor Layer 统一入口

版本:
V5-dev

说明:
本模块作为财务因子、估值因子、技术因子之间的适配层。

设计原则:
1. 不修改已有因子计算逻辑
2. 不替代 financial_factor.py / valuation.py / technical.py
3. 只负责统一调用和输出结构

"""

from typing import Dict, Optional


def build_factor_snapshot(
    code: str,
    financial_factor: Optional[Dict] = None,
    valuation_score: Optional[float] = None,
    technical_score: Optional[float] = None,
) -> Dict:
    """
    构建单股票因子快照。

    参数:
        code:
            股票代码

        financial_factor:
            financial_factor.calculate_financial_factor()
            输出结果中的财务因子信息

        valuation_score:
            valuation.calculate_valuation_score()
            输出的估值评分

        technical_score:
            technical.build_technical()
            输出的技术评分

    返回:
        统一 Factor Layer 数据结构
    """

    return {
        "code": code,

        "financial": financial_factor or {},

        "valuation": {
            "valuation_score": valuation_score
        }
        if valuation_score is not None
        else {},

        "technical": {
            "technical_score": technical_score
        }
        if technical_score is not None
        else {},
    }


def extract_stock_score_inputs(snapshot: Dict) -> Dict:
    """
    转换为 stock_score.py 所需输入。

    保持评分层和因子层分离。
    """

    financial = snapshot.get("financial", {})

    valuation = snapshot.get("valuation", {})

    technical = snapshot.get("technical", {})

    return {
        "code": snapshot.get("code"),

        "financial_factor": financial,

        "valuation_score": valuation.get(
            "valuation_score"
        ),

        "technical_score": technical.get(
            "technical_score"
        ),
    }
