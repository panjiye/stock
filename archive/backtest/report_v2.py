import pandas as pd
import numpy as np
import os


# ============================================================
# 参数
# ============================================================

EQUITY_FILE = "results/equity.csv"
TRADES_FILE = "results/trades.csv"

REPORT_FILE = "results/report.txt"


INITIAL_CAPITAL = 1000000



# ============================================================
# 收益指标
# ============================================================


def calculate_return(equity):

    start = equity.iloc[0]["total_value"]

    end = equity.iloc[-1]["total_value"]


    total_return = (
        end / start - 1
    )


    return total_return





def calculate_annual_return(
        equity
):

    start_date = pd.to_datetime(
        equity.iloc[0]["date"]
    )

    end_date = pd.to_datetime(
        equity.iloc[-1]["date"]
    )


    years = (
        end_date - start_date
    ).days / 365


    if years <= 0:

        return 0


    total_return = calculate_return(
        equity
    )


    annual = (
        (1 + total_return)
        **
        (1 / years)
        -
        1
    )


    return annual




# ============================================================
# 风险指标
# ============================================================


def calculate_drawdown(equity):


    value = equity["total_value"]


    high = value.cummax()


    drawdown = (
        value - high
    ) / high


    return drawdown.min()



def calculate_volatility(equity):


    daily_return = (
        equity["total_value"]
        .pct_change()
        .dropna()
    )


    return (
        daily_return.std()
        *
        np.sqrt(252)
    )



def calculate_sharpe(equity):


    daily_return = (
        equity["total_value"]
        .pct_change()
        .dropna()
    )


    if len(daily_return)==0:

        return 0


    return (
        daily_return.mean()
        /
        daily_return.std()
        *
        np.sqrt(252)
    )





# ============================================================
# 交易统计
# ============================================================


def analyze_trades(
        trades
):


    result={}


    if len(trades)==0:

        return {


            "count":0

        }



    sells = trades[
        trades["action"]=="SELL"
    ].copy()



    result["count"] = len(sells)



    if len(sells)==0:

        return result



    returns=[]


    for code,group in sells.groupby("code"):


        buy = group[
            group["action"]=="BUY"
        ]

        sell = group[
            group["action"]=="SELL"
        ]


        if len(buy)==0:

            continue


        buy_price = (
            buy.iloc[0]["price"]
        )

        sell_price = (
            sell.iloc[-1]["price"]
        )


        r = (
            sell_price
            /
            buy_price
            -
            1
        )


        returns.append(
            r
        )



    if len(returns)==0:

        return result



    returns=np.array(
        returns
    )



    result["win"] = int(
        (returns>0).sum()
    )


    result["loss"] = int(
        (returns<=0).sum()
    )


    result["win_rate"] = (
        result["win"]
        /
        len(returns)
    )



    result["avg_profit"] = (

        returns[
            returns>0
        ].mean()

        if

        (returns>0).any()

        else

        0
    )



    result["avg_loss"] = (

        returns[
            returns<=0
        ].mean()

        if

        (returns<=0).any()

        else

        0

    )



    result["max_profit"] = (
        returns.max()
    )


    result["max_loss"] = (
        returns.min()
    )



    if result["avg_loss"] != 0:

        result["profit_loss_ratio"] = (

            result["avg_profit"]
            /
            abs(
                result["avg_loss"]
            )

        )

    else:

        result["profit_loss_ratio"]=0



    return result




# ============================================================
# 生成报告
# ============================================================


def generate_report():



    print("="*60)

    print(
        "读取回测结果..."
    )



    equity=pd.read_csv(
        EQUITY_FILE
    )


    trades=pd.read_csv(
        TRADES_FILE
    )



    total_return = calculate_return(
        equity
    )


    annual_return = calculate_annual_return(
        equity
    )


    drawdown = calculate_drawdown(
        equity
    )


    volatility = calculate_volatility(
        equity
    )


    sharpe = calculate_sharpe(
        equity
    )


    trade_info = analyze_trades(
        trades
    )



    final_value = (
        equity.iloc[-1]
        ["total_value"]
    )



    lines=[]


    lines.append(
        "="*60
    )

    lines.append(
        "量化回测报告"
    )

    lines.append(
        "="*60
    )


    lines.append("")


    lines.append(
        "资金:"
    )


    lines.append(
        f"初始资金: {INITIAL_CAPITAL:,.2f}"
    )


    lines.append(
        f"最终资产: {final_value:,.2f}"
    )


    lines.append(
        f"累计收益: {total_return*100:.2f}%"
    )


    lines.append(
        f"年化收益: {annual_return*100:.2f}%"
    )


    lines.append("")


    lines.append(
        "风险:"
    )


    lines.append(
        f"最大回撤: {drawdown*100:.2f}%"
    )


    lines.append(
        f"年化波动: {volatility*100:.2f}%"
    )


    lines.append(
        f"夏普比率: {sharpe:.2f}"
    )


    lines.append("")


    lines.append(
        "交易:"
    )


    lines.append(
        f"交易次数: {trade_info.get('count',0)}"
    )


    if "win_rate" in trade_info:


        lines.append(
            f"胜率: {trade_info['win_rate']*100:.2f}%"
        )


        lines.append(
            f"平均盈利: {trade_info['avg_profit']*100:.2f}%"
        )


        lines.append(
            f"平均亏损: {trade_info['avg_loss']*100:.2f}%"
        )


        lines.append(
            f"盈亏比: {trade_info['profit_loss_ratio']:.2f}"
        )


        lines.append(
            f"最大盈利: {trade_info['max_profit']*100:.2f}%"
        )


        lines.append(
            f"最大亏损: {trade_info['max_loss']*100:.2f}%"
        )



    text="\n".join(
        lines
    )



    print(text)



    os.makedirs(
        "results",
        exist_ok=True
    )


    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(text)



    print()

    print(
        "报告保存:",
        REPORT_FILE
    )




if __name__=="__main__":

    generate_report()