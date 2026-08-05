import sqlite3
import pandas as pd

from backtest.risk_stock_exit import StockRiskExit


conn = sqlite3.connect(
    "database/stock.db"
)


price = pd.read_sql(
    """
    select
        date,
        code,
        close
    from daily_price_qfq
    where code='600410'
    order by date
    """,
    conn
)



indicator = pd.read_sql(
    """
    select
        date,
        code,
        MA60
    from daily_indicator
    where code='600410'
    order by date
    """,
    conn
)



technical = pd.read_sql(
    """
    select
        date,
        code,
        ma120
    from technical_factor
    where code='600410'
    order by date
    """,
    conn
)



df = (
    price
    .merge(
        indicator,
        on=["date","code"]
    )
    .merge(
        technical,
        on=["date","code"]
    )
)



# 字段统一

df.rename(
    columns={
        "ma120":"MA120"
    },
    inplace=True
)



risk = StockRiskExit()



result = risk.check_stock(
    "600410",
    12.08,
    df
)



print(result)