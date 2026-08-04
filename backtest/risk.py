import pandas as pd
import sqlite3


DB_PATH = "database/stock.db"



class MarketRisk:

    """
    市场风险控制

    根据沪深300 MA200
    返回目标仓位

    """

    def __init__(
        self,
        code="000300.SH"
    ):

        self.code = code

        self.market = self.load_market()



    def load_market(self):

        conn = sqlite3.connect(
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


        df["ma200"] = (
            df["close"]
            .rolling(200)
            .mean()
        )


        df["below_days"] = (
            df["close"]
            <
            df["ma200"]
        ).astype(int)


        df["below_days"] = (
            df["below_days"]
            .groupby(
                (
                    df["below_days"]
                    !=
                    df["below_days"].shift()
                ).cumsum()
            )
            .cumsum()
        )


        return df



    def get_position_ratio(
        self,
        date
    ):


        row = self.market[
            self.market["date"]
            <=
            pd.Timestamp(date)
        ]


        if len(row)==0:

            return 1.0


        row=row.iloc[-1]



        # 数据不足200天

        if pd.isna(
            row["ma200"]
        ):

            return 1.0



        # 深度熊市

        if (
            row["close"]
            <
            row["ma200"]

            and

            row["below_days"]
            >=60
        ):

            return 0.2



        # 普通熊市

        if (
            row["close"]
            <
            row["ma200"]
        ):

            return 0.5



        return 1.0