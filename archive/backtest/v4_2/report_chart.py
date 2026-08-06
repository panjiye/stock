import pandas as pd
import matplotlib.pyplot as plt
import os
from data.query import engine



EQUITY_FILE = "results/equity.csv"

REPORT_DIR = "results/report"





# =====================================================
# 读取策略
# =====================================================

def load_equity():

    df = pd.read_csv(
        EQUITY_FILE
    )


    df["date"] = pd.to_datetime(
        df["date"]
    )


    df = df.sort_values(
        "date"
    )


    return df





# =====================================================
# 读取指数
# =====================================================

def load_index(
    code="000300.SH"
):


    conn = engine.connect(
        DB_PATH
    )


    df=pd.read_sql(
        f"""
        select
            date,
            close
        from index_price
        where code='{code}'
        order by date
        """,
        conn
    )


    conn.close()


    df["date"]=pd.to_datetime(
        df["date"]
    )


    return df





# =====================================================
# 资金曲线
# =====================================================

def plot_equity(
    equity
):


    plt.figure(
        figsize=(12,5)
    )


    plt.plot(
        equity["date"],
        equity["total_value"]
    )


    plt.title(
        "Strategy Equity Curve"
    )


    plt.xlabel(
        "Date"
    )


    plt.ylabel(
        "Value"
    )


    plt.grid()


    plt.tight_layout()


    plt.savefig(
        f"{REPORT_DIR}/equity_curve.png",
        dpi=150
    )


    plt.close()





# =====================================================
# 回撤
# =====================================================

def plot_drawdown(
    equity
):


    value=equity["total_value"]


    high=value.cummax()


    dd=(value/high-1)*100



    plt.figure(
        figsize=(12,4)
    )


    plt.plot(
        equity["date"],
        dd
    )


    plt.title(
        "Drawdown"
    )


    plt.ylabel(
        "%"
    )


    plt.grid()


    plt.tight_layout()


    plt.savefig(
        f"{REPORT_DIR}/drawdown.png",
        dpi=150
    )


    plt.close()




# =====================================================
# 年收益
# =====================================================

def plot_yearly(
    equity
):


    df=equity.copy()


    df["year"]=(
        df["date"]
        .dt.year
    )


    yearly=[]


    for y,g in df.groupby(
        "year"
    ):

        ret=(
            g["total_value"].iloc[-1]
            /
            g["total_value"].iloc[0]
            -
            1
        )*100


        yearly.append(
            [y,ret]
        )



    data=pd.DataFrame(
        yearly,
        columns=[
            "year",
            "return"
        ]
    )



    plt.figure(
        figsize=(12,5)
    )


    plt.bar(
        data["year"],
        data["return"]
    )


    plt.title(
        "Yearly Return"
    )


    plt.ylabel(
        "%"
    )


    plt.grid(
        axis="y"
    )


    plt.tight_layout()


    plt.savefig(
        f"{REPORT_DIR}/yearly_return.png",
        dpi=150
    )


    plt.close()





# =====================================================
# 超额收益
# =====================================================

def plot_excess(
    equity
):


    index=load_index()



    df=pd.merge(
        equity[
            [
                "date",
                "total_value"
            ]
        ],

        index,

        on="date",

        how="inner"

    )



    df["strategy"]=(

        df["total_value"]

        /

        df["total_value"].iloc[0]

    )


    df["benchmark"]=(

        df["close"]

        /

        df["close"].iloc[0]

    )


    df["excess"]=(
        df["strategy"]
        /
        df["benchmark"]
    )



    plt.figure(
        figsize=(12,5)
    )


    plt.plot(
        df["date"],
        df["excess"]
    )


    plt.title(
        "Excess Return vs CSI300"
    )


    plt.grid()


    plt.tight_layout()


    plt.savefig(
        f"{REPORT_DIR}/excess_return.png",
        dpi=150
    )


    plt.close()




# =====================================================
# main
# =====================================================

def main():

    os.makedirs(
        REPORT_DIR,
        exist_ok=True
    )


    equity=load_equity()



    plot_equity(
        equity
    )


    plot_drawdown(
        equity
    )


    plot_yearly(
        equity
    )


    plot_excess(
        equity
    )


    print("="*60)

    print(
        "图形报告生成完成"
    )

    print("="*60)





if __name__=="__main__":

    main()