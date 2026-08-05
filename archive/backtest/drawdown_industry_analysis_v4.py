# backtest/drawdown_industry_analysis_v4.py

import os
import pandas as pd
from data.query import engine


RESULT_DIR = "results_v4_2"


# ============================================================
# 读取数据
# ============================================================

def load_equity():

    path = os.path.join(
        RESULT_DIR,
        "equity.csv"
    )

    df = pd.read_csv(path)

    df["date"] = pd.to_datetime(df["date"])

    if "total_value" in df.columns:
        df["equity"] = df["total_value"]

    elif "equity" in df.columns:
        pass

    else:
        raise Exception(
            "equity.csv不存在资产字段"
        )

    return df



def get_max_drawdown_period():

    equity = load_equity()

    equity = equity.sort_values(
        "date"
    )

    equity["high"] = (
        equity["equity"]
        .cummax()
    )

    equity["drawdown"] = (
        equity["equity"]
        /
        equity["high"]
        -1
    )

    end_idx = (
        equity["drawdown"]
        .idxmin()
    )

    high_value = (
        equity.loc[:end_idx,"equity"]
        .max()
    )

    start_idx = (
        equity[
            equity.index <= end_idx
        ]["equity"]
        .idxmax()
    )

    start = equity.loc[
        start_idx,
        "date"
    ]

    end = equity.loc[
        end_idx,
        "date"
    ]

    dd = (
        equity.loc[
            end_idx,
            "drawdown"
        ]
        *
        100
    )


    return start,end,dd



# ============================================================
# 股票行业
# ============================================================

def load_industry():

    conn = engine.connect(
        DB_PATH
    )

    df = pd.read_sql(
        """
        select
        code,
        name,
        industry
        from stock_industry
        """,
        conn
    )

    conn.close()


    df["code"] = (
        df["code"]
        .astype(str)
        .str.zfill(6)
    )


    return df



# ============================================================
# 股票亏损
# ============================================================

def load_stocks():

    path = os.path.join(
        RESULT_DIR,
        "drawdown_stocks.csv"
    )


    df = pd.read_csv(path)


    df["code"] = (
        df["code"]
        .astype(str)
        .str.zfill(6)
    )


    return df



# ============================================================
# 行业分析
# ============================================================

def industry_analysis():

    print("="*70)
    print("最大回撤行业归因分析 v4")
    print("="*70)


    start,end,dd = (
        get_max_drawdown_period()
    )


    print()
    print("最大回撤:")
    print(
        f"开始: {start}"
    )
    print(
        f"结束: {end}"
    )
    print(
        f"幅度: {dd:.2f}%"
    )


    stocks = load_stocks()

    industry = load_industry()


    df = stocks.merge(
        industry,
        on="code",
        how="left"
    )


    df["industry"] = (
        df["industry"]
        .fillna(
            "未知"
        )
    )


    result = (
        df
        .groupby(
            "industry"
        )
        .agg(

            股票数量=(
                "code",
                "count"
            ),

            总持股=(
                "shares",
                "sum"
            ),

            平均收益=(
                "return",
                "mean"
            ),

            最差收益=(
                "return",
                "min"
            )

        )
        .sort_values(
            "平均收益"
        )
    )


    print()

    print(
        result.head(30)
    )


    csv_path=os.path.join(
        RESULT_DIR,
        "drawdown_industry.csv"
    )


    result.to_csv(
        csv_path,
        encoding="utf-8-sig"
    )



    txt_path=os.path.join(
        RESULT_DIR,
        "drawdown_industry.txt"
    )


    with open(
        txt_path,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "最大回撤行业归因分析\n"
        )

        f.write(
            "="*50+"\n\n"
        )

        f.write(
            f"开始:{start}\n"
        )

        f.write(
            f"结束:{end}\n"
        )

        f.write(
            f"回撤:{dd:.2f}%\n\n"
        )


        f.write(
            result
            .to_string()
        )


    print()
    print(
        "生成完成"
    )

    print(
        csv_path
    )

    print(
        txt_path
    )



if __name__=="__main__":

    industry_analysis()