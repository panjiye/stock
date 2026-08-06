import json
import time
import subprocess
from pathlib import Path
from html import escape

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sqlalchemy import text

from backtest.advanced_metrics import calculate_drawdown_period, monthly_return, yearly_return
from data.query import engine
from strategy.strategy_pipeline import select_strategy_stocks



# ============================================================
# 参数
# ============================================================

INITIAL_CAPITAL = 1000000

# 修改:
# 原 TOP100
# 改为 TOP50
TOP_N = 50


# 回测开始时间
BACKTEST_START = "2005-01-01"


# 最少股票数量
MIN_STOCK_COUNT = 30

# 调仓周期
REBALANCE_FREQUENCY = "quarterly"

# 手续费率 / 滑点（当前回测尚未应用成本模型，置 0 如实标注）
FEE_RATE = 0.0
SLIPPAGE = 0.0

# 因子版本
FACTOR_VERSION = "v5.0"



# ============================================================
# 读取因子数据
# ============================================================


def load_factor_score():


    print()
    print("=" * 60)
    print("读取 factor_score...")


    start=time.time()


    sql=text(
        """
        SELECT

            code,
            pub_date,
            stat_date,
            final_score

        FROM factor_score

        WHERE

            pub_date IS NOT NULL

        AND

            stat_date >= :start_date


        ORDER BY

            code,
            stat_date

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(
            sql,
            conn,
            params={
                "start_date":
                BACKTEST_START
            }
        )


    print(
        "因子记录:",
        len(df)
    )


    print(
        "耗时:",
        round(time.time()-start,2),
        "秒"
    )


    df["pub_date"]=(
        pd.to_datetime(
            df["pub_date"],
            errors="coerce",
            format="mixed"
        )
    )


    df["stat_date"]=(
        pd.to_datetime(
            df["stat_date"],
            errors="coerce",
            format="mixed"
        )
    )


    return df



# ============================================================
# 读取季度调仓日期
# ============================================================


def get_rebalance_dates(df):


    dates=(

        df["stat_date"]

        .drop_duplicates()

        .sort_values()

        .tolist()

    )


    return dates



# ============================================================
# 根据公告日期筛选股票
# ============================================================


def select_stocks(
        factor,
        rebalance_date
):


    print()

    print(
        "筛选日期:",
        rebalance_date.strftime("%Y-%m-%d")
    )


    available=factor[

        factor["pub_date"]
        <=
        rebalance_date

    ].copy()



    print(
        "可用因子:",
        len(available)
    )



    if len(available)==0:

        return []



    available=(

        available

        .sort_values(
            [
                "code",
                "stat_date"
            ]
        )

        .groupby(
            "code"
        )

        .tail(1)

    )



    stock_count=len(available)


    # 新增:
    # 股票太少不交易

    if stock_count < MIN_STOCK_COUNT:

        print(
            "股票数量不足:",
            stock_count
        )

        return []



    result = select_strategy_stocks(

        available,

        TOP_N

    )


    print(
        "选股数量:",
        len(result)
    )


    return result



# ============================================================
# 获取下一交易日
# ============================================================


def get_next_trade_day(date):


    sql=text(
        """
        SELECT

            MIN(date) AS date

        FROM daily_price_qfq

        WHERE

            date > :date

        """
    )


    with engine.connect() as conn:

        df=pd.read_sql(

            sql,

            conn,

            params={

                "date":

                date.strftime("%Y-%m-%d")

            }

        )


    if df.empty:

        return None


    return pd.to_datetime(

        df.iloc[0]["date"]

    )



# ============================================================
# 获取最近交易日价格（当日或之前最近一个交易日）
# ============================================================


def get_nearest_price(stocks, target_date):
    """
    批量获取 target_date 当日或之前最近一个交易日的价格。

    用于处理季度调仓日 / 卖出日不是交易日的场景，
    避免精确日期匹配导致整期数据缺失（EMPTY_CLOSE）。
    """
    if len(stocks) == 0:
        return pd.DataFrame()

    if not isinstance(target_date, pd.Timestamp):
        target_date = pd.to_datetime(target_date)

    placeholders = ",".join([f":c{i}" for i in range(len(stocks))])
    t = target_date.strftime("%Y-%m-%d")

    sql = f"""
    SELECT p.code, p.date, p.open, p.close
    FROM daily_price_qfq p
    INNER JOIN
    (
        SELECT code, MAX(date) AS nearest_date
        FROM daily_price_qfq
        WHERE code IN ({placeholders}) AND date <= :t
        GROUP BY code
    ) m
        ON p.code = m.code AND p.date = m.nearest_date
    WHERE p.code IN ({placeholders}) AND p.date <= :t
    """

    params = {f"c{i}": c for i, c in enumerate(stocks)}
    params["t"] = t

    with engine.connect() as conn:
        df = pd.read_sql(text(sql), conn, params=params)

    df["date"] = pd.to_datetime(df["date"])

    return df


def get_nearest_trade_price(stock_code, target_date):
    """
    获取单只股票 target_date 当日或之前最近一个交易日的价格。

    返回行包含 code / date / open / close，
    若不存在任何可交易价格则返回空 DataFrame。
    """
    t = pd.to_datetime(target_date).strftime("%Y-%m-%d")

    sql = text(
        """
        SELECT code, date, open, close
        FROM daily_price_qfq
        WHERE code = :c AND date <= :d
        ORDER BY date DESC
        LIMIT 1
        """
    )

    with engine.connect() as conn:
        df = pd.read_sql(sql, conn, params={"c": stock_code, "d": t})

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])

    return df


# ============================================================
# 获取买入价格（当日或之前最近交易日）
# ============================================================


def get_open_price(
        stocks,
        date
):


    if len(stocks)==0:

        return pd.DataFrame()


    nearest = get_nearest_price(
        stocks,
        date
    )

    if nearest.empty:

        return pd.DataFrame()


    df = nearest[["code", "open"]].copy()

    df=df[

        df["open"]>0

    ]


    return df



# ============================================================
# 获取卖出价格
# ============================================================


def get_close_price(
        stocks,
        date
):


    if len(stocks)==0:

        return pd.DataFrame()


    nearest = get_nearest_price(
        stocks,
        date
    )

    if nearest.empty:

        return pd.DataFrame()


    df = nearest[["code", "close"]].copy()

    df=df[

        df["close"]>0

    ]


    return df
# ============================================================
# 回测核心
# ============================================================


def run_backtest(factor):


    rebalance_dates = get_rebalance_dates(
        factor
    )


    print()
    print("=" * 60)
    print(
        "开始季度多因子回测"
    )

    print(
        "调仓季度:",
        len(rebalance_dates)
    )


    cash = INITIAL_CAPITAL


    equity_curve=[]

    trades=[]

    holdings=[]

    rebalance_records=[]

    coverage=[]


    for i, rebalance_date in enumerate(
            rebalance_dates[:-1]
    ):


        # 每个理论季度调仓日都生成一条 coverage 记录，禁止静默跳过
        coverage_row = {
            "rebalance_date": rebalance_date.strftime("%Y-%m-%d"),
            "has_factor_score": False,
            "stock_count": 0,
            "status": "NO_FACTOR",
            "actual_rebalance": False,
        }

        print()
        print("-"*60)


        print(
            "调仓:",
            rebalance_date.strftime("%Y-%m-%d")
        )


        buy_date=get_next_trade_day(
            rebalance_date
        )


        if buy_date is None:

            coverage_row["status"] = "NO_BUY_DATE"
            coverage.append(coverage_row)
            print(
                " [coverage] 无后续交易日: NO_BUY_DATE"
            )
            continue



        stocks=select_stocks(
            factor,
            rebalance_date
        )


        if len(stocks)==0:

            coverage_row["status"] = "EMPTY_STOCKS"
            coverage.append(coverage_row)
            print(
                " [coverage] 股票数量不足被跳过: EMPTY_STOCKS"
            )
            continue


        # 有可用因子且选股非空
        coverage_row["has_factor_score"] = True
        coverage_row["stock_count"] = len(stocks)
        coverage_row["status"] = "OK"
        coverage_row["actual_rebalance"] = True


        print(
            "买入日期:",
            buy_date.strftime("%Y-%m-%d")
        )



        buy_price=get_open_price(
            stocks,
            buy_date
        )


        if len(buy_price)==0:

            coverage_row["actual_rebalance"] = False
            coverage_row["status"] = "EMPTY_OPEN"
            coverage.append(coverage_row)
            print(
                " [coverage] 无有效买入价格: EMPTY_OPEN"
            )
            continue



        sell_date=rebalance_dates[i+1]



        sell_price=get_close_price(
            stocks,
            sell_date
        )



        if len(sell_price)==0:

            coverage_row["actual_rebalance"] = False
            coverage_row["status"] = "EMPTY_CLOSE"
            coverage.append(coverage_row)
            print(
                " [coverage] 无有效卖出价格: EMPTY_CLOSE"
            )
            continue



        portfolio = buy_price.merge(

            sell_price,

            on="code",

            suffixes=(

                "_buy",

                "_sell"

            )

        )



        if len(portfolio)==0:

            coverage_row["actual_rebalance"] = False
            coverage_row["status"] = "EMPTY_MERGE"
            coverage.append(coverage_row)
            print(
                " [coverage] 买卖价无交集: EMPTY_MERGE"
            )
            continue


        coverage.append(coverage_row)



        portfolio["return"]=(

            portfolio["close"]

            /

            portfolio["open"]

            -

            1

        )



        period_return=(

            portfolio["return"]

            .mean()

        )



        cash = cash * (

            1+

            period_return

        )



        for code in stocks:
            row = portfolio[portfolio["code"] == code]
            if len(row) == 0:
                continue
            holdings.append(
                {
                    "rebalance_date": rebalance_date.strftime("%Y-%m-%d"),
                    "code": code,
                    "return": float(row.iloc[0]["return"]),
                    "weight": 1.0 / len(stocks),
                }
            )

        trades.append(

            {

                "buy_date":
                    buy_date.strftime(
                        "%Y-%m-%d"
                    ),

                "sell_date":
                    sell_date.strftime(
                        "%Y-%m-%d"
                    ),

                "stocks":
                    len(portfolio),

                "return":
                    period_return,

                "value":
                    cash

            }

        )



        equity_curve.append(

            {

                "date":
                    sell_date.strftime(
                        "%Y-%m-%d"
                    ),

                "value":
                    cash

            }

        )

        rebalance_records.append(
            {
                "rebalance_date": rebalance_date.strftime("%Y-%m-%d"),
                "stock_count": len(stocks),
                "turnover": 1.0,
                "value": cash,
            }
        )


        print(
            "成交股票:",
            len(portfolio)
        )


        print(
            "季度收益:",
            round(
                period_return*100,
                2
            ),
            "%"
        )


        print(
            "资产:",
            round(
                cash,
                2
            )
        )



    return (

        pd.DataFrame(equity_curve),

        pd.DataFrame(trades),

        pd.DataFrame(holdings),

        pd.DataFrame(rebalance_records),

        pd.DataFrame(coverage),

    )




# ============================================================
# 性能指标
# ============================================================


def calculate_performance(
        equity
):


    if len(equity)==0:

        return {}



    equity=equity.copy()



    equity["date"]=pd.to_datetime(

        equity["date"]

    )



    equity=equity.sort_values(

        "date"

    )



    values=(

        equity["value"]

        .astype(float)

    )



    initial=INITIAL_CAPITAL


    final=values.iloc[-1]



    total_return=(

        final

        /

        initial

        -

        1

    )



    # 修改:
    # 使用真实日期计算年数

    days=(

        equity["date"].iloc[-1]

        -

        equity["date"].iloc[0]

    ).days



    years=max(

        days/365,

        0.1

    )



    annual_return=(

        (final/initial)

        **

        (1/years)

        -

        1

    )



    max_value=(

        values

        .cummax()

    )



    drawdown=(

        values

        /

        max_value

        -

        1

    )


    max_drawdown=drawdown.min()



    quarterly_return=(

        values

        .pct_change()

        .dropna()

    )



    if len(quarterly_return)>1:


        sharpe=(

            quarterly_return.mean()

            /

            quarterly_return.std()

            *

            np.sqrt(4)

        )

    else:

        sharpe=0



    return {


        "initial_capital":

            initial,


        "final_value":

            float(final),


        "total_return":

            float(total_return),


        "annual_return":

            float(annual_return),


        "max_drawdown":

            float(max_drawdown),


        "sharpe":

            float(sharpe)

    }




# ============================================================
# 主程序
# ============================================================


def build_dashboard_assets(
        output_dir,
        equity,
        trades,
        holdings,
        rebalance_records,
        coverage,
        metrics,
        params
):

    output_dir = Path(output_dir)
    dashboard_dir = output_dir / "dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)

    dashboard_data = {
        "metrics": metrics,
        "params": params,
        "summary": {
            "equity_rows": int(len(equity)),
            "trade_rows": int(len(trades)),
            "holding_rows": int(len(holdings)),
            "rebalance_rows": int(len(rebalance_records)),
            "coverage_rows": int(len(coverage)),
            "coverage_ok": int((coverage["actual_rebalance"] == True).sum()) if not coverage.empty else 0,  # noqa: E712
            "coverage_skipped": int((coverage["actual_rebalance"] != True).sum()) if not coverage.empty else 0,  # noqa: E712
        },
    }

    with open(dashboard_dir / "dashboard_data.json", "w", encoding="utf-8") as f:
        json.dump(dashboard_data, f, ensure_ascii=False, indent=2)

    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>V5.0 Beta Dashboard</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #123; }}
    .card {{ border: 1px solid #dbe4ee; border-radius: 10px; padding: 16px; margin-bottom: 16px; background: #f8fbff; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }}
    .metric {{ background: white; padding: 12px; border-radius: 8px; border: 1px solid #e1e8f0; }}
    code {{ background: #eef4fb; padding: 2px 4px; border-radius: 4px; }}
  </style>
</head>
<body>
  <h1>V5.0 Beta Dashboard</h1>
  <p>Minimal web view for the current research baseline.</p>
  <div class=\"card\">
    <h2>Summary</h2>
    <div class=\"grid\">
      <div class=\"metric\"><strong>Final Value</strong><br/>{metrics.get('final_value', 0):,.2f}</div>
      <div class=\"metric\"><strong>Max Drawdown</strong><br/>{metrics.get('max_drawdown', 0):.2%}</div>
      <div class=\"metric\"><strong>Sharpe</strong><br/>{metrics.get('sharpe', 0):.4f}</div>
      <div class=\"metric\"><strong>Trades</strong><br/>{len(trades)}</div>
      <div class=\"metric\"><strong>Holdings</strong><br/>{len(holdings)}</div>
      <div class=\"metric\"><strong>Rebalances</strong><br/>{len(rebalance_records)}</div>
      <div class=\"metric\"><strong>Coverage OK/Skipped</strong><br/>{int((coverage['actual_rebalance'] == True).sum())}/{int((coverage['actual_rebalance'] != True).sum())}</div>
    </div>
  </div>
  <div class=\"card\">
    <h2>Baseline Files</h2>
    <ul>
      <li><a href=\"../equity.csv\">equity.csv</a></li>
      <li><a href=\"../trades.csv\">trades.csv</a></li>
      <li><a href=\"../holdings.csv\">holdings.csv</a></li>
      <li><a href=\"../rebalance_records.csv\">rebalance_records.csv</a></li>
      <li><a href=\"../coverage.csv\">coverage.csv</a></li>
      <li><a href=\"../params.json\">params.json</a></li>
      <li><a href=\"../REPORT.md\">REPORT.md</a></li>
      <li><a href=\"../charts/equity_curve.png\">charts/equity_curve.png</a></li>
    </ul>
  </div>
  <div class=\"card\">
    <h2>Parameters</h2>
    <pre>{escape(json.dumps(params, ensure_ascii=False, indent=2))}</pre>
  </div>
</body>
</html>
"""

    with open(dashboard_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(html)

    return dashboard_dir


def build_baseline_outputs(
        output_dir,
        equity,
        trades,
        holdings,
        rebalance_records,
        coverage,
        metrics,
        params
):

    output_dir = Path(output_dir)
    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    charts_dir = output_dir / "charts"
    charts_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    if not equity.empty:
        equity.to_csv(
            output_dir / "equity.csv",
            index=False
        )
    else:
        pd.DataFrame(columns=["date", "value"]).to_csv(
            output_dir / "equity.csv",
            index=False
        )

    if not trades.empty:
        trades.to_csv(
            output_dir / "trades.csv",
            index=False
        )
    else:
        pd.DataFrame(columns=["buy_date", "sell_date", "stocks", "return", "value"]).to_csv(
            output_dir / "trades.csv",
            index=False
        )

    if not holdings.empty:
        holdings.to_csv(
            output_dir / "holdings.csv",
            index=False
        )
    else:
        pd.DataFrame(columns=["rebalance_date", "code", "return", "weight"]).to_csv(
            output_dir / "holdings.csv",
            index=False
        )

    if not rebalance_records.empty:
        rebalance_records.to_csv(
            output_dir / "rebalance_records.csv",
            index=False
        )
    else:
        pd.DataFrame(columns=["rebalance_date", "stock_count", "turnover", "value"]).to_csv(
            output_dir / "rebalance_records.csv",
            index=False
        )

    # coverage.csv: 完整理论季度调仓记录，禁止静默跳过
    if not coverage.empty:
        coverage.to_csv(
            output_dir / "coverage.csv",
            index=False
        )
    else:
        pd.DataFrame(
            columns=["rebalance_date", "has_factor_score", "stock_count", "status", "actual_rebalance"]
        ).to_csv(
            output_dir / "coverage.csv",
            index=False
        )

    with open(
        output_dir / "params.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            params,
            f,
            ensure_ascii=False,
            indent=2
        )

    equity["date"] = pd.to_datetime(equity["date"])
    equity = equity.sort_values("date")

    plt.figure(figsize=(12, 5))
    plt.plot(equity["date"], equity["value"])
    plt.title("Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(charts_dir / "equity_curve.png", dpi=150)
    plt.close()

    drawdown = (equity["value"] / equity["value"].cummax() - 1) * 100
    plt.figure(figsize=(12, 4))
    plt.plot(equity["date"], drawdown)
    plt.title("Drawdown")
    plt.xlabel("Date")
    plt.ylabel("%")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(charts_dir / "drawdown.png", dpi=150)
    plt.close()

    yearly = yearly_return(equity, "value")
    plt.figure(figsize=(12, 5))
    plt.bar(yearly["year"].astype(str), yearly["return"])
    plt.title("Yearly Return")
    plt.xlabel("Year")
    plt.ylabel("%")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(charts_dir / "yearly_return.png", dpi=150)
    plt.close()

    monthly = monthly_return(equity, "value")
    if not monthly.empty:
        monthly["year"] = monthly["month"].str[:4].astype(int)
        monthly["month_num"] = monthly["month"].str[5:7].astype(int)
        heatmap = monthly.pivot(index="year", columns="month_num", values="return")
        heatmap = heatmap.sort_index()
        fig, ax = plt.subplots(figsize=(12, 4))
        im = ax.imshow(heatmap.values, cmap="RdYlGn", aspect="auto")
        ax.set_xticks(range(len(heatmap.columns)))
        ax.set_xticklabels([str(x).zfill(2) for x in heatmap.columns])
        ax.set_yticks(range(len(heatmap.index)))
        ax.set_yticklabels([str(x) for x in heatmap.index])
        ax.set_title("Monthly Return Heatmap")
        ax.set_xlabel("Month")
        ax.set_ylabel("Year")
        for r in range(heatmap.shape[0]):
            for c in range(heatmap.shape[1]):
                value = heatmap.iloc[r, c]
                if pd.notna(value):
                    ax.text(c, r, f"{value:.1f}", ha="center", va="center")
        fig.colorbar(im, ax=ax)
        fig.tight_layout()
        fig.savefig(charts_dir / "monthly_return_heatmap.png", dpi=150)
        plt.close(fig)
    else:
        plt.figure(figsize=(12, 4))
        plt.text(0.5, 0.5, "No monthly return data", ha="center", va="center")
        plt.axis("off")
        plt.savefig(charts_dir / "monthly_return_heatmap.png", dpi=150)
        plt.close()

    turnover = rebalance_records[["rebalance_date", "turnover"]].copy()
    if not turnover.empty:
        turnover["rebalance_date"] = pd.to_datetime(turnover["rebalance_date"])
        turnover = turnover.sort_values("rebalance_date")
        plt.figure(figsize=(12, 4))
        plt.plot(turnover["rebalance_date"], turnover["turnover"])
        plt.title("Turnover")
        plt.xlabel("Date")
        plt.ylabel("Turnover")
        plt.grid(alpha=0.3)
        plt.tight_layout()
        plt.savefig(charts_dir / "turnover.png", dpi=150)
        plt.close()
    else:
        plt.figure(figsize=(12, 4))
        plt.text(0.5, 0.5, "No turnover data", ha="center", va="center")
        plt.axis("off")
        plt.savefig(charts_dir / "turnover.png", dpi=150)
        plt.close()

    # ---- 计算 coverage 概要（用于 REPORT 与 dashboard）----
    coverage_summary = {
        "total": int(len(coverage)) if not coverage.empty else 0,
        "ok": int((coverage["actual_rebalance"] == True).sum()) if not coverage.empty else 0,  # noqa: E712
        "skipped": int((coverage["actual_rebalance"] != True).sum()) if not coverage.empty else 0,  # noqa: E712
        "has_factor": int((coverage["has_factor_score"] == True).sum()) if not coverage.empty else 0,  # noqa: E712
    }
    if not coverage.empty:
        coverage_status_count = coverage["status"].value_counts().to_dict()
    else:
        coverage_status_count = {}

    report_lines = [
        "# V5.0 Beta Baseline Report",
        "",
        "## 说明（流程验证声明）",
        "- 本回测为 V5.0 Beta 基线，目标在于打通 data → factor → strategy → backtest → result 完整链路。",
        "- **当前回测结果仅用于流程验证，不构成任何策略有效性或投资结论。**",
        "- 在消除技术因子未来函数、补齐数据缺口之前，所有收益/回撤/Sharpe 指标均只作为研究中间产物。",
        "",
        "## Strategy",
        "- Baseline V5 strategy uses factor_score ranking with quarterly rebalance and a simple top-N stock selection pipeline.",
        "- Selection is based on the current factor_score table and the existing strategy_pipeline interface.",
        "",
        "## Data Range",
        f"- Factor data loaded from {params.get('backtest_start', 'unknown')} onward.",
        f"- Backtest end (factor coverage): {params.get('backtest_end', 'unknown')}.",
        f"- Output directory: {output_dir}",
        "",
        "## Factor Description",
        "- The pipeline uses the current financial, valuation and technical factor scores from factor_score.",
        "- Technical factor logic remains unchanged in this baseline release.",
        "",
        "## Backtest Period",
        f"- Initial capital: {params.get('initial_capital', 0):,.0f}",
        f"- Top N: {params.get('top_n', 0)}",
        f"- Minimum stock count: {params.get('min_stock_count', 0)}",
        f"- Rebalance frequency: {params.get('rebalance_frequency', 'quarterly')}",
        f"- Fee rate: {params.get('fee_rate', 0.0)}",
        f"- Slippage: {params.get('slippage', 0.0)}",
        "",
        "## Performance Metrics",
        f"- Final value: {metrics.get('final_value', 0):,.2f}",
        f"- Total return: {metrics.get('total_return', 0):.2%}",
        f"- Annual return: {metrics.get('annual_return', 0):.2%}",
        f"- Max drawdown: {metrics.get('max_drawdown', 0):.2%}",
        f"- Sharpe: {metrics.get('sharpe', 0):.4f}",
        "",
        "## Data Coverage",
        f"- Theoretical quarterly rebalance periods: {coverage_summary['total']}",
        f"- Actually rebalanced: {coverage_summary['ok']}",
        f"- Skipped (not rebalanced): {coverage_summary['skipped']}",
        f"- Periods with usable factor score: {coverage_summary['has_factor']}",
        f"- Status breakdown: {coverage_status_count}",
        "- 详细逐期记录见 coverage.csv（含每期有无因子、股票数量、是否实际调仓、跳过原因）。",
        "",
        "## Known Limitations",
        "- 本基线为可运行的首版交付物，未经完整实证校验。",
        "- 技术因子未来函数未修复：historical point 可能使用全序列分位，存在未来数据污染风险。",
        "- 卖出价/买入价已改为「target_date 当日或之前最近交易日」匹配 daily_price_qfq，EMPTY_CLOSE 导致的非连续时间轴已修复；coverage.csv 中仅剩边界期 EMPTY_STOCKS（回测起点无可用因子）。",
        "- 采用等权组合，未计入手续费、滑点、涨跌停、停牌等真实交易约束。",
        "- 大量缺失季度通过 coverage.csv 显式记录，不再静默跳过。",
        "- holdings / rebalance 为最小化记录，供下游分析使用。",
    ]

    with open(output_dir / "REPORT.md", "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    build_dashboard_assets(
        output_dir,
        equity,
        trades,
        holdings,
        rebalance_records,
        coverage,
        metrics,
        params,
    )

    print()
    print("标准结果目录:", output_dir)

    return output_dir


def collect_environment_info(factor):
    """
    收集用于 params.json 的运行环境信息（不修改数据库）：

    - git commit
    - database 版本（核心表数据最大日期汇总）
    - factor 数据起止日期
    """

    # git commit
    git_commit = "unknown"
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
            cwd=str(Path(__file__).resolve().parents[1]),
        )
        if result.returncode == 0 and result.stdout.strip():
            git_commit = result.stdout.strip()
    except Exception:
        git_commit = "unknown"

    # database 版本：核心表 max(date) 汇总
    db_version = {}
    query_map = {
        "daily_price_qfq": "SELECT MAX(date) AS m FROM daily_price_qfq",
        "financial_profit": "SELECT MAX(stat_date) AS m FROM financial_profit",
        "factor_score": "SELECT MAX(stat_date) AS m FROM factor_score",
        "technical_quarter_factor": "SELECT MAX(stat_date) AS m FROM technical_quarter_factor",
        "stock_pool": "SELECT MAX(date) AS m FROM stock_pool",
    }
    for table, sql in query_map.items():
        try:
            with engine.connect() as conn:
                df = pd.read_sql(text(sql), conn)
            val = df.iloc[0]["m"] if not df.empty else None
            db_version[table] = (str(val) if pd.notna(val) else None)
        except Exception:
            db_version[table] = None

    # factor 数据起止
    backtest_end = "unknown"
    factor_start = "unknown"
    if factor is not None and not factor.empty:
        backtest_end = factor["stat_date"].max().strftime("%Y-%m-%d")
        factor_start = factor["stat_date"].min().strftime("%Y-%m-%d")

    return {
        "git_commit": git_commit,
        "database_version": db_version,
        "factor_data_start": factor_start,
        "backtest_end": backtest_end,
    }


def main():


    factor=load_factor_score()



    equity, trades, holdings, rebalance_records, coverage = run_backtest(

        factor

    )



    result=calculate_performance(

        equity

    )


    # 收集运行环境信息（git commit / database 版本 / 数据范围）
    env_info = collect_environment_info(factor)

    params = {
        "initial_capital": INITIAL_CAPITAL,
        "top_n": TOP_N,
        "min_stock_count": MIN_STOCK_COUNT,
        "backtest_start": BACKTEST_START,
        "backtest_end": env_info["backtest_end"],
        "factor_data_start": env_info["factor_data_start"],
        "rebalance_frequency": REBALANCE_FREQUENCY,
        "fee_rate": FEE_RATE,
        "slippage": SLIPPAGE,
        "strategy": "factor_score_top_n_quarterly",
        "factor_version": FACTOR_VERSION,
        "database_version": env_info["database_version"],
        "git_commit": env_info["git_commit"],
    }



    print()

    print("="*60)

    print(
        "回测完成"
    )


    print(result)



    print()

    print(
        "交易次数:",
        len(trades)
    )



    if len(trades)>0:


        print()

        print(
            trades.head()
        )



    output_dir = Path(__file__).resolve().parents[1] / "results" / "v5" / "v5.0_baseline"

    build_baseline_outputs(
        output_dir,
        equity,
        trades,
        holdings,
        rebalance_records,
        coverage,
        result,
        params,
    )




if __name__=="__main__":

    main()