import pandas as pd


class Portfolio:
    """
    组合管理

    管理:

    cash
    positions
    equity history

    """

    def __init__(
        self,
        initial_cash=1000000
    ):

        self.initial_cash = initial_cash

        self.cash = initial_cash


        # 
        # {
        #   code:
        #       {
        #          shares:
        #          cost:
        #       }
        # }
        #

        self.positions = {}


        self.history = []



    # ==================================================
    # 持仓数量
    # ==================================================

    def has_position(
        self,
        code
    ):

        return code in self.positions



    # ==================================================
    # 买入
    # ==================================================

    def buy(
        self,
        code,
        shares,
        price,
        cost
    ):

        amount = (
            shares *
            price
        )


        total_cost = (
            amount
            +
            cost
        )


        if total_cost > self.cash:

            return False



        self.cash -= total_cost



        if code in self.positions:


            old = self.positions[code]


            old_amount = (
                old["shares"]
                *
                old["cost"]
            )


            new_amount = (
                shares
                *
                price
            )


            total_shares = (
                old["shares"]
                +
                shares
            )


            avg_cost = (
                old_amount
                +
                new_amount
            ) / total_shares



            self.positions[code]={
                "shares":
                    total_shares,

                "cost":
                    avg_cost
            }



        else:


            self.positions[code]={

                "shares":
                    shares,

                "cost":
                    price

            }



        return True





    # ==================================================
    # 卖出
    # ==================================================

    def sell(
        self,
        code,
        price,
        cost
    ):


        if code not in self.positions:

            return None



        position = self.positions[code]


        shares = position["shares"]



        amount = (
            shares
            *
            price
        )


        self.cash += (
            amount
            -
            cost
        )


        del self.positions[code]


        return shares





    # ==================================================
    # 当前市值
    # ==================================================

    def market_value(
        self,
        prices
    ):


        value = 0


        for code,pos in self.positions.items():


            if code in prices:


                value += (
                    pos["shares"]
                    *
                    prices[code]
                )


        return value




    # ==================================================
    # 总资产
    # ==================================================

    def total_value(
        self,
        prices
    ):


        return (

            self.cash

            +

            self.market_value(
                prices
            )

        )





    # ==================================================
    # 每日记录
    # ==================================================

    def record(
        self,
        date,
        prices
    ):


        value=self.total_value(
            prices
        )


        self.history.append(

            {

                "date":
                    date,

                "cash":
                    self.cash,

                "stock_value":
                    self.market_value(
                        prices
                    ),

                "total_value":
                    value

            }

        )



    def get_history(
        self
    ):


        return pd.DataFrame(
            self.history
        )