import os
import pandas as pd
from data.query import engine


RESULT_DIR = "results_v4_2"



STOCK_FILE = os.path.join(
    RESULT_DIR,
    "drawdown_stocks.csv"
)


OUTPUT_CSV = os.path.join(
    RESULT_DIR,
    "drawdown_industry.csv"
)

OUTPUT_TXT = os.path.join(
    RESULT_DIR,
    "drawdown_industry.txt"
)



def load_industry():

    conn = engine.connect(DB_PATH)

    df = pd.read_sql(
        """
        select
            code,
            industry
        from stock_industry
        """,
        conn
    )

    conn.close()

    return df



def analyze():


    print("="*70)
    print("最大回撤行业归因分析")
    print("="*70)


    stocks = pd.read_csv(
        STOCK_FILE,
        dtype={
            "code":str
        }
    )


    industry = load_industry()


    # 补充6位代码
    stocks["code"] = (
        stocks["code"]
        .astype(str)
        .str.zfill(6)
    )


    df = stocks.merge(
        industry,
        on="code",
        how="left"
    )


    df["industry"] = (
        df["industry"]
        .fillna("未知")
    )


    result = (
        df
        .groupby("industry")
        .agg(
            股票数量=("code","count"),
            总持股=("shares","sum"),
            平均收益=("return","mean"),
            最差收益=("return","min")
        )
        .sort_values(
            "平均收益"
        )
    )


    result.to_csv(
        OUTPUT_CSV,
        encoding="utf-8-sig"
    )


    with open(
        OUTPUT_TXT,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "最大回撤行业归因分析\n"
        )

        f.write(
            "="*60+"\n\n"
        )


        f.write(
            result.to_string()
        )


    print()
    print(result.head(20))


    print()
    print("生成完成")
    print(OUTPUT_CSV)
    print(OUTPUT_TXT)



if __name__ == "__main__":

    analyze()