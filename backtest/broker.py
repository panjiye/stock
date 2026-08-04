from backtest.cost import TradeCost



class Broker:
    """
    成交模拟

    买入:
        open

    卖出:
        close

    """


    def __init__(self):


        self.cost = TradeCost()



    # ==================================================
    # 买入价格
    # ==================================================

    def buy_price(
        self,
        price
    ):


        return self.cost.buy_price(
            price
        )



    # ==================================================
    # 卖出价格
    # ==================================================

    def sell_price(
        self,
        price
    ):


        return self.cost.sell_price(
            price
        )




    # ==================================================
    # 买入费用
    # ==================================================

    def buy_cost(
        self,
        amount
    ):


        return self.cost.buy_cost(
            amount
        )




    # ==================================================
    # 卖出费用
    # ==================================================

    def sell_cost(
        self,
        amount
    ):


        return self.cost.sell_cost(
            amount
        )



    # ==================================================
    # 股票数量
    # A股100股整数
    # ==================================================

    def calculate_shares(
        self,
        cash,
        price
    ):


        if price<=0:

            return 0



        shares = int(
            cash /
            price /
            100
        ) * 100



        return shares