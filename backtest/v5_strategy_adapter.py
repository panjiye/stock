"""
V5 Strategy Adapter

作用：
将 Strategy Layer(V5) 输出转换为 Backtest 所需信号格式。

设计原则：
- 不修改 engine_v4_2
- 不修改 trader / portfolio
- 只负责接口适配
"""

from typing import Dict, List


def convert_strategy_signal_to_backtest_signal(
    strategy_signal: Dict,
    trade_date,
    close_price: float,
) -> Dict:
    """将单个策略信号转换为回测信号格式。"""

    action = strategy_signal.get("signal", "HOLD")

    return {
        "date": trade_date,
        "code": strategy_signal.get("code"),
        "action": action,
        "close": float(close_price),
        "reason": strategy_signal.get("reason", []),
    }


def convert_strategy_signals(
    strategy_signals: List[Dict],
    trade_date,
    price_map: Dict,
) -> List[Dict]:
    """批量转换策略信号。"""

    result = []

    for item in strategy_signals:
        code = item.get("code")

        if code not in price_map:
            continue

        result.append(
            convert_strategy_signal_to_backtest_signal(
                item,
                trade_date,
                price_map[code],
            )
        )

    return result
