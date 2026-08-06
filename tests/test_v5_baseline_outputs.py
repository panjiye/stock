from pathlib import Path

import pandas as pd

from scripts.backtest_factor import build_baseline_outputs


def test_build_baseline_outputs_writes_required_files(tmp_path):
    equity = pd.DataFrame(
        [
            {"date": "2024-01-01", "value": 1000000.0},
            {"date": "2024-04-01", "value": 1100000.0},
        ]
    )
    trades = pd.DataFrame(
        [{"buy_date": "2024-01-01", "sell_date": "2024-04-01", "return": 0.1}]
    )
    holdings = pd.DataFrame(
        [{"rebalance_date": "2024-01-01", "code": "000001", "return": 0.1, "weight": 1.0}]
    )
    rebalance_records = pd.DataFrame(
        [{"rebalance_date": "2024-01-01", "stock_count": 1, "turnover": 1.0, "value": 1000000.0}]
    )
    coverage = pd.DataFrame(
        [
            {
                "rebalance_date": "2024-01-01",
                "has_factor_score": True,
                "stock_count": 1,
                "status": "OK",
                "actual_rebalance": True,
            }
        ]
    )
    metrics = {"final_value": 1100000.0, "max_drawdown": -0.05, "sharpe": 1.2}
    params = {"initial_capital": 1000000, "top_n": 50}

    output_dir = build_baseline_outputs(
        tmp_path,
        equity,
        trades,
        holdings,
        rebalance_records,
        coverage,
        metrics,
        params,
    )

    assert output_dir == tmp_path
    assert (output_dir / "equity.csv").exists()
    assert (output_dir / "trades.csv").exists()
    assert (output_dir / "holdings.csv").exists()
    assert (output_dir / "rebalance_records.csv").exists()
    assert (output_dir / "coverage.csv").exists()
    assert (output_dir / "params.json").exists()
    assert (output_dir / "REPORT.md").exists()
    assert (output_dir / "charts").exists()
    assert (output_dir / "charts" / "equity_curve.png").exists()

