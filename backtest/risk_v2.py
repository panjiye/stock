import pandas as pd
from data.query import engine





class MarketRisk:

    """
    市场风险控制 v2

    综合:
    1. MA200趋势
    2. 趋势偏离程度
    3. 20日波动率

    输出:
    0.2 - 1.0 动态仓位

    """

    def __init__(
        self,
        code="000300.SH"
    ):

        self.code = code

        self.market = self.load_market()



    def load_market(self):

        conn = engine.connect(
            DB_PATH
        )


        df = pd.read_sql(
            f"""
            select
                date,
                close
            from index_price
            where code='{self.code}'
            order by date
            """,
            conn
        )


        conn.close()


        df["date"] = pd.to_datetime(
            df["date"]
        )


        # 200日均线

        df["ma200"] = (
            df["close"]
            .rolling(200)
            .mean()
        )


        # 趋势距离

        df["trend"] = (
            df["close"]
            /
            df["ma200"]
            -
            1
        )


        # 日收益

        df["return"] = (
            df["close"]
            .pct_change()
        )


        # 20日波动

        df["volatility"] = (
            df["return"]
            .rolling(20)
            .std()
            *
            (252 ** 0.5)
        )


        return df



    def get_position_ratio(
        self,
        date
    ):

        data = self.market[
            self.market["date"]
            <=
            pd.Timestamp(date)
        ]


        if len(data) == 0:

            return 1.0



        row = data.iloc[-1]



        # 数据不足

        if pd.isna(row["ma200"]):

            return 1.0



        trend = row["trend"]

        volatility = row["volatility"]



        # -----------------------
        # 趋势评分
        # -----------------------

        if trend >= 0.10:

            trend_score = 1.0


        elif trend >= 0:

            trend_score = 0.8


        elif trend >= -0.05:

            trend_score = 0.6


        elif trend >= -0.15:

            trend_score = 0.4


        else:

            trend_score = 0.2



        # -----------------------
        # 波动率调整
        # -----------------------

        if pd.isna(volatility):

            vol_score = 1.0


        elif volatility < 0.20:

            vol_score = 1.0


        elif volatility < 0.30:

            vol_score = 0.8


        elif volatility < 0.40:

            vol_score = 0.6


        else:

            vol_score = 0.4



        # -----------------------
        # 综合仓位
        # -----------------------

        position = (
            trend_score
            *
            vol_score
        )


        # 限制范围

        position = max(
            0.2,
            min(
                1.0,
                position
            )
        )


        return round(
            position,
            2
        )