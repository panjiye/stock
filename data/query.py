"""
V5 Data Query Layer

负责：

SQLite数据库访问

架构：

database
    |
    v
data.query
    |
    v
analysis / factor / strategy / backtest


注意：

不要在业务模块直接操作数据库。
"""

import os

import pandas as pd
from sqlalchemy import create_engine, text


# ==================================================
# Database
# ==================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DB_FILE = os.path.join(
    BASE_DIR,
    "database",
    "stock.db"
)
DB_PATH = DB_FILE

engine = create_engine(
    f"sqlite:///{DB_FILE}"
)


# ==================================================
# Index
# ==================================================

def get_index_daily(code):
    """
    获取指数日线数据

    Parameters
    ----------
    code:
        指数代码

        支持:
        000300
        000300.SH

    Returns
    -------
    DataFrame
    """

    if "." not in code:
        code = code + ".SH"


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
        FROM index_price
        WHERE code=:code
        ORDER BY date
        """
    )


    with engine.connect() as conn:

        df = pd.read_sql(
            sql,
            conn,
            params={
                "code": code
            }
        )


    return df



# ==================================================
# Stock Price
# ==================================================

def get_stock_daily(code):
    """
    获取单只股票前复权日线数据

    Parameters
    ----------
    code:
        股票代码

    Returns
    -------
    DataFrame
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
                "code": code
            }
        )


    return df



# ==================================================
# Stock Basic
# ==================================================

def get_stock_list():
    """
    获取股票列表

    Returns
    -------
    DataFrame
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



# ==================================================
# Latest Price
# ==================================================

def get_latest_price():
    """
    获取所有股票最新交易日行情

    Returns
    -------
    DataFrame
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