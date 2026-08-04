from backtest.cost import TradeCost

cost = TradeCost()

def check_sell(df):

    """
    卖出判断

    当前规则:

    收盘价跌破 MA20

    """

    if len(df) < 20:
        return False


    latest = df.iloc[-1]


    if latest["close"] < latest["MA20"]:

        return True


    return False





def run_backtest(df, signals):

    """
    模拟交易


    买入:
    使用 signal.py 产生的信号


    卖出:

    1.
    持仓超过10天

    2.
    close < MA20

    3.
    跌破买入价8%止损

    """


    trades=[]


    position=False


    buy_date=None

    buy_price=None

    buy_index=None
    buy_amount=None


    signal_dates = {

        x["date"]

        for x in signals

    }



    for i in range(60,len(df)):


        current = df.iloc[:i+1]


        today = df.iloc[i]



        # =====================
        # 空仓
        # =====================

        if not position:


            if today["date"] in signal_dates:


                position=True


                buy_date=today["date"]


                buy_price=float(
                    cost.buy_price(today["close"])
                )


                buy_amount=100000


                buy_fee=cost.buy_cost(
                    buy_amount
                )


                buy_index=i



        # =====================
        # 持仓
        # =====================

        else:


            hold_days = i - buy_index


            stop_loss = (
                today["close"]
                <
                buy_price * 0.92
            )


            trend_break = (
                hold_days >= 10
                and
                check_sell(current)
            )


            if stop_loss or trend_break:


                sell_date=today["date"]


                sell_price=float(
                    cost.sell_price(today["close"])
                )


                sell_amount = (
                    buy_amount
                    *
                    sell_price
                    /
                    buy_price
                )


                sell_fee = cost.sell_cost(
                    sell_amount
                )


                real_profit = (
                    sell_amount
                    -
                    sell_fee
                    -
                    buy_amount
                    -
                    buy_fee
                )


                profit = (
                    real_profit
                    /
                    (buy_amount + buy_fee)
                    *
                    100
                )



                trades.append(
                    {

                        "buy_date":buy_date,


                        "buy_price":round(
                            buy_price,
                            2
                        ),


                        "sell_date":sell_date,


                        "sell_price":round(
                            sell_price,
                            2
                        ),


                        "return":round(
                            profit,
                            2
                        )

                    }
                )


                position=False


                buy_date=None

                buy_price=None

                buy_index=None

                buy_amount=None

    return trades