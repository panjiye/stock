"""
个股风险退出模块 v1

功能:
检测持仓股票是否需要退出

规则:

1. 跌破MA60持续20天
2. 跌破MA120持续10天
3. 单股亏损超过30%

输入:
portfolio:
    {
        code:
            {
                shares,
                cost
            }
    }


prices:
DataFrame

date
code
close
MA60
MA120


输出:

[
 {
   code,
   action,
   reason,
   date
 }
]

"""


import pandas as pd



class StockRiskExit:


    def __init__(
        self,
        ma60_days=20,
        ma120_days=10,
        max_loss=-0.30
    ):

        self.ma60_days = ma60_days
        self.ma120_days = ma120_days
        self.max_loss = max_loss



    def check_stock(
        self,
        code,
        cost,
        df
    ):


        df=df.sort_values("date").copy()


        if len(df)==0:
            return None


        latest=df.iloc[-1]


        close=latest.close


        current_return = (
            close-cost
        ) / cost



        #
        # 规则3 最大亏损
        #
        if current_return <= self.max_loss:

            return {

                "code":code,

                "action":"SELL",

                "reason":
                f"亏损超过{abs(self.max_loss):.0%}",

                "date":
                latest.date

            }



        #
        # MA60检查
        #

        if "MA60" in df.columns:


            below60 = (
                df.close <
                df.MA60
            )


            if (
                below60
                .tail(self.ma60_days)
                .all()
            ):


                return {


                    "code":code,

                    "action":"SELL",

                    "reason":
                    f"跌破MA60超过{self.ma60_days}天",

                    "date":
                    latest.date
                }



        #
        # MA120检查
        #

        if "MA120" in df.columns:


            below120 = (
                df.close <
                df.MA120
            )


            if (
                below120
                .tail(self.ma120_days)
                .all()
            ):


                return {


                    "code":code,

                    "action":"SELL",

                    "reason":
                    f"跌破MA120超过{self.ma120_days}天",

                    "date":
                    latest.date
                }


        return None



    def check_portfolio(
        self,
        portfolio,
        prices
    ):


        exits=[]


        for code, position in portfolio.items():


            stock_price = prices[
                prices.code==code
            ]


            if len(stock_price)==0:
                continue



            result=self.check_stock(

                code,

                position["cost"],

                stock_price

            )


            if result:

                exits.append(result)



        return pd.DataFrame(exits)