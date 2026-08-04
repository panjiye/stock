"""
交易成本模型

包括：
1. 佣金
2. 印花税
3. 过户费
4. 滑点
"""


class TradeCost:

    def __init__(
        self,
        commission_rate=0.0003,
        stamp_tax_rate=0.001,
        transfer_rate=0.00001,
        min_commission=5,
        slippage=0.001
    ):

        # 买卖佣金
        self.commission_rate = commission_rate

        # 卖出印花税
        self.stamp_tax_rate = stamp_tax_rate

        # 过户费
        self.transfer_rate = transfer_rate

        # 最低佣金
        self.min_commission = min_commission

        # 滑点
        self.slippage = slippage


    def buy_price(self, price):
        """
        买入实际成交价格
        """

        return price * (1 + self.slippage)


    def sell_price(self, price):
        """
        卖出实际成交价格
        """

        return price * (1 - self.slippage)



    def buy_cost(self, amount):
        """
        买入交易费用

        amount:
        成交金额
        """

        commission = max(
            amount * self.commission_rate,
            self.min_commission
        )

        return commission



    def sell_cost(self, amount):
        """
        卖出交易费用

        包含：
        佣金
        印花税
        过户费
        """

        commission = max(
            amount * self.commission_rate,
            self.min_commission
        )

        stamp_tax = (
            amount *
            self.stamp_tax_rate
        )

        transfer = (
            amount *
            self.transfer_rate
        )


        return (
            commission
            +
            stamp_tax
            +
            transfer
        )