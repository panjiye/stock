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

def insert_ignore(
    df,
    table
):
    """
    DataFrame 忽略重复键写入
    """

    if df is None:
        return 0


    if df.empty:
        return 0


    columns = list(df.columns)

    cols = ",".join(columns)

    placeholders = ",".join(
        [
            f":{c}"
            for c in columns
        ]
    )


    sql = text(
        f"""
        INSERT OR IGNORE INTO {table}
        (
            {cols}
        )
        VALUES
        (
            {placeholders}
        )
        """
    )


    records = df.to_dict(
        orient="records"
    )


    with engine.begin() as conn:

        result = conn.execute(
            sql,
            records
        )


    return result.rowcount

# def upsert_dataframe(
#     df,
#     table,
#     unique_columns
# ):
#     """
#     DataFrame 插入或更新

#     sqlite INSERT OR REPLACE 替代方案
#     """

#     if df is None:
#         return 0

#     if df.empty:
#         return 0


#     columns = list(df.columns)


#     placeholders = ",".join(
#         [f":{c}" for c in columns]
#     )


#     column_sql = ",".join(
#         columns
#     )


#     update_columns = [
#         c for c in columns
#         if c not in unique_columns
#     ]


#     update_sql = ",".join(
#         [
#             f"{c}=excluded.{c}"
#             for c in update_columns
#         ]
#     )


#     sql = f"""
#     INSERT INTO {table}
#     (
#         {column_sql}
#     )
#     VALUES
#     (
#         {placeholders}
#     )
#     ON CONFLICT
#     (
#         {",".join(unique_columns)}
#     )
#     DO UPDATE SET
#     {update_sql}
#     """


#     with engine.begin() as conn:

#         conn.execute(
#             text(sql),
#             df.to_dict(
#                 orient="records"
#             )
#         )


#     return len(df)

def upsert_dataframe(
    df,
    table,
    unique_columns
):
    """
    dataframe 批量 upsert

    使用 sqlite ON CONFLICT
    """

    if df is None:
        return 0

    if df.empty:
        return 0


    columns = list(df.columns)


    update_columns = [
        c for c in columns
        if c not in unique_columns
    ]


    placeholders = ",".join(
        [f":{c}" for c in columns]
    )


    update_sql = ",".join(
        [
            f"{c}=excluded.{c}"
            for c in update_columns
        ]
    )


    conflict = ",".join(
        unique_columns
    )


    sql = f"""
    INSERT INTO {table}
    (
        {",".join(columns)}
    )
    VALUES
    (
        {placeholders}
    )
    ON CONFLICT
    (
        {conflict}
    )
    DO UPDATE SET
    {update_sql}
    """


    records = df.to_dict(
        orient="records"
    )


    with engine.begin() as conn:

        conn.execute(
            text(sql),
            records
        )


    return len(records)