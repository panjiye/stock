import sqlite3
import pandas as pd

from backtest.risk_stock_exit_v2 import apply_stock_exit


DB = "database/stock.db"
def apply_stock_exit(
    trades,
    prices,
    indicator
):

    results=[]

    for _, row in trades.iterrows():

        result = check_exit(
            row.buy_date,
            row.code,
            row.buy_price,
            prices,
            indicator
        )

        if result:

            result.update(
                {
                    "code":row.code,
                    "buy_date":row.buy_date,
                    "buy_price":row.buy_price
                }
            )

            results.append(result)


    return pd.DataFrame(results)

def load_data():

    conn = sqlite3.connect(DB)


    trades = pd.read_sql(
        """
        select
            code,
            buy_date,
            buy_price,
            shares
        from trades
        """,
        conn
    )


    prices = pd.read_sql(
        """
        select
            code,
            date,
            close
        from daily_price
        """,
        conn
    )


    indicator = pd.read_sql(
        """
        select
            code,
            date,
            MA60
        from daily_indicator
        """,
        conn
    )


    conn.close()


    return trades, prices, indicator



def main():

    trades, prices, indicator = load_data()


    print("交易数量:", len(trades))


    result = apply_stock_exit(
        trades,
        prices,
        indicator
    )


    print()
    print("退出完成")
    print()


    print(
        result["exit_reason"]
        .value_counts()
    )


    print()


    print(
        result[
            [
                "return",
                "pnl"
            ]
        ]
        .describe()
    )


    output = (
        "results_v4_2/"
        "risk_stock_exit_v2.csv"
    )


    result.to_csv(
        output,
        index=False,
        encoding="utf-8-sig"
    )


    print()
    print("输出:")
    print(output)



if __name__ == "__main__":

    main()