import time
import akshare as ak

from data.writer import insert_ignore
from data.writer import insert_dataframe

INDEX_LIST = {

    "000300.SH": {
        "symbol": "sh000300",
        "name": "沪深300"
    },


    "000905.SH": {
        "symbol": "sh000905",
        "name": "中证500"
    },


    "000852.SH": {
        "symbol": "sh000852",
        "name": "中证1000"
    },


    "399006.SZ": {
        "symbol": "sz399006",
        "name": "创业板指"
    },


    "000001.SH": {
        "symbol": "sh000001",
        "name": "上证指数"
    }

}



def download_index(symbol):


    df = ak.stock_zh_index_daily(
        symbol=symbol
    )


    if df.empty:

        return None



    if "amount" not in df.columns:

        df["amount"] = 0



    return df[
        [
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount"
        ]
    ]


def save_index(
    code,
    df
):

    df = df.copy()

    df["code"] = code


    df = df[
        [
            "code",
            "date",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "amount"
        ]
    ]


    return insert_ignore(
        df,
        "index_price"
    )

def main():


    print("="*60)

    print("开始下载指数数据")

    print("="*60)



    for code,item in INDEX_LIST.items():


        print()

        print(
            "下载:",
            item["name"],
            code
        )


        try:


            df = download_index(
                item["symbol"]
            )


            if df is None:


                print(
                    "无数据"
                )

                continue



            print(
                "行情数量:",
                len(df)
            )



            n = save_index(
                code,
                df
            )


            print(
                "写入:",
                n
            )



        except Exception as e:


            print(
                "失败:",
                e
            )


        time.sleep(1)



    print()

    print("="*60)

    print("完成")

    print("="*60)





if __name__ == "__main__":

    main()