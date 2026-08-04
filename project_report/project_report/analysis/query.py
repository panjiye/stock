import pandas as pd
from sqlalchemy import create_engine,text
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


db_file = os.path.join(
    BASE_DIR,
    "database",
    "stock.db"
)


engine = create_engine(
    f"sqlite:///{db_file}"
)



def get_stock_daily(code):

    """
    获取单只股票全部日线数据
    """

    sql = text(
        """
        SELECT
            date,
            open,
            high,
            low,
            close,
            volume,
            amount,
            code
        FROM daily_price_qfq
        WHERE code=:code
        ORDER BY date
        """
    )


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn,
            params={
                "code":code
            }
        )


    return df



def get_stock_list():

    """
    获取股票列表
    """

    sql = text(
        """
        SELECT
            code,
            name
        FROM stock_basic
        WHERE status='1'
        ORDER BY code
        """
    )


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn
        )


    return df



def get_latest_price():

    """
    获取所有股票最新交易日数据
    """


    sql = text(
        """
        SELECT
            a.*
        FROM daily_price_qfq a

        INNER JOIN
        (
            SELECT
                code,
                MAX(date) AS max_date
            FROM daily_price_qfq
            GROUP BY code
        ) b

        ON a.code=b.code
        AND a.date=b.max_date
        """
    )


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn
        )


    return df