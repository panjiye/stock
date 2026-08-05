from datetime import datetime

import pandas as pd
import tushare as ts

from config.tushare_config import TUSHARE_TOKEN

from data.writer import upsert_dataframe



def get_engine():

    return ts.pro_api(
        TUSHARE_TOKEN
    )



def download_industry():

    print("=" * 60)
    print("开始下载股票行业分类(Tushare)")
    print("=" * 60)


    pro = get_engine()


    print("获取股票基础信息...")


    df = pro.stock_basic(
        exchange="",
        list_status="L",
        fields=
        """
        ts_code,
        symbol,
        name,
        industry
        """
    )


    print(
        f"股票数量: {len(df)}"
    )


    update_date = datetime.now().strftime(
        "%Y-%m-%d"
    )


    df = df.rename(
        columns={
            "symbol": "code"
        }
    )


    df["industry"] = (
        df["industry"]
        .fillna("")
    )


    df["source"] = "tushare"

    df["update_date"] = update_date


    df = df[
        [
            "code",
            "name",
            "industry",
            "source",
            "update_date"
        ]
    ]


    count = upsert_dataframe(
        df,
        "stock_industry",
        [
            "code"
        ]
    )


    print()

    print("=" * 60)

    print(
        f"写入完成: {count}"
    )

    print("=" * 60)



if __name__ == "__main__":

    download_industry()