import pandas as pd
from sqlalchemy import text

from data.query import engine


def insert_dataframe(
    df,
    table,
    if_exists="append"
):
    """
    DataFrame 写入数据库

    参数:
        df:
            pandas DataFrame

        table:
            表名

        if_exists:
            append / replace
    """

    if df is None:
        return


    if df.empty:
        return


    df.to_sql(
        table,
        engine,
        if_exists=if_exists,
        index=False
    )



def execute_sql(
    sql,
    params=None
):
    """
    执行 SQL
    """

    with engine.begin() as conn:

        result = conn.execute(
            text(sql),
            params or {}
        )

    return result



def get_connection():

    """
    获取数据库连接

    用于复杂事务
    """

    return engine.connect()
