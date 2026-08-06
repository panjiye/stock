import pandas as pd


# ============================
# 参数
# ============================

BUY_COMMISSION = 0.0003

SELL_COMMISSION = 0.0003

STAMP_TAX = 0.001

SLIPPAGE = 0.001


INITIAL_CAPITAL = 1000000



def main():


    print("="*60)
    print("读取交易记录")


    trades = pd.read_csv(
        "backtest_trades.csv"
    )


    print(
        "交易次数:",
        len(trades)
    )



    capital = INITIAL_CAPITAL


    result=[]



    for _, row in trades.iterrows():


        period_return = row["return"]


        # 买入成本
        buy_cost = (
            BUY_COMMISSION
            +
            SLIPPAGE
        )


        # 卖出成本
        sell_cost = (
            SELL_COMMISSION
            +
            STAMP_TAX
            +
            SLIPPAGE
        )



        net_return = (

            1
            +
            period_return

        ) * (

            1-buy_cost

        ) * (

            1-sell_cost

        ) - 1



        capital = (

            capital
            *
            (1+net_return)

        )



        result.append(

            {

            "buy_date":
                row["buy_date"],


            "sell_date":
                row["sell_date"],


            "stocks":
                row["stocks"],


            "gross_return":
                period_return,


            "net_return":
                net_return,


            "value":
                capital

            }

        )



    df=pd.DataFrame(
        result
    )


    df.to_csv(
        "backtest_equity_cost.csv",
        index=False
    )


    print("="*60)

    print(
        "成本计算完成"
    )


    print(
        "最终资产:",
        capital
    )



if __name__=="__main__":

    main()