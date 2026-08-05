import pandas as pd
import akshare as ak
import baostock as bs

from sqlalchemy import text

from data.query import engine



# =========================
# 测试股票
# =========================

TEST_STOCKS = [
    "600519",   # 贵州茅台
    "600000",   # 浦发银行
    "300750",   # 宁德时代
]


# =========================
# 从本地数据库读取东方财富数据
# =========================


def load_local_financial(code):

    sql = text(
        """
        SELECT

            code,

            stat_date,

            roe_avg,

            np_margin,

            gp_margin,

            net_profit,

            eps_ttm,

            main_business_revenue


        FROM financial_profit

        WHERE code=:code

        ORDER BY stat_date DESC

        LIMIT 5
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



# =========================
# AkShare
# =========================


def get_akshare_profit(code):

    print("\n获取 AkShare:", code)


    try:

        df = ak.stock_financial_report_sina(
            stock=code,
            symbol="利润表"
        )


        return df.head(10)


    except Exception as e:

        print(
            "AkShare失败:",
            e
        )

        return None



# =========================
# Baostock
# =========================


def get_baostock_profit(code):

    print("\n获取 Baostock:", code)


    try:

        bs.login()


        market_code = (
            "sh."
            +
            code
            if code.startswith("6")
            else
            "sz."
            +
            code
        )


        rs = bs.query_profit_data(
            code=market_code,
            year=2025,
            quarter=4
        )


        rows=[]


        while rs.next():

            rows.append(
                rs.get_row_data()
            )


        bs.logout()


        if len(rows)==0:

            return None


        return pd.DataFrame(
            rows,
            columns=rs.fields
        )


    except Exception as e:

        print(
            "Baostock失败:",
            e
        )

        return None



# =========================
# 主程序
# =========================


def main():


    for code in TEST_STOCKS:


        print("\n")
        print("="*60)

        print(
            "股票:",
            code
        )


        print("\n")
        print(
            "====== 本地 financial_profit ======"
        )


        local = load_local_financial(
            code
        )


        print(local)



        print("\n")
        print(
            "====== AkShare ======"
        )


        ak_df = get_akshare_profit(
            code
        )


        if ak_df is not None:

            print(
                ak_df.head()
            )



        print("\n")
        print(
            "====== Baostock ======"
        )


        bs_df = get_baostock_profit(
            code
        )


        if bs_df is not None:

            print(
                bs_df.head()
            )



if __name__=="__main__":

    main()