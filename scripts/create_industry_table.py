"""
创建股票行业分类表

table:
stock_industry

用途:
- 行业归因分析
- 行业中性化
- 行业轮动研究

"""

from sqlalchemy import text

from analysis.query import engine


def create_table():

    sql = """

    CREATE TABLE IF NOT EXISTS stock_industry
    (

        code TEXT PRIMARY KEY,

        name TEXT,

        industry TEXT,

        source TEXT,

        update_date TEXT

    );

    """


    with engine.begin() as conn:

        conn.execute(
            text(sql)
        )


    print("=" * 60)
    print("stock_industry 表创建完成")
    print("=" * 60)



if __name__ == "__main__":

    create_table()