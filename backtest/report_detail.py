import pandas as pd
import os


EQUITY_FILE = "results/equity.csv"


OUTPUT_DIR = "results/report"



# ======================================================
# 年度收益
# ======================================================

def generate_yearly_return(
    equity
):

    df = equity.copy()

    df["date"] = pd.to_datetime(
        df["date"]
    )


    df["year"] = (
        df["date"]
        .dt.year
    )


    rows=[]


    for year,g in df.groupby(
        "year"
    ):

        start = (
            g["total_value"]
            .iloc[0]
        )

        end = (
            g["total_value"]
            .iloc[-1]
        )


        ret = (
            end/start-1
        )*100


        rows.append(
            {
                "year":year,
                "return":round(ret,2)
            }
        )


    result=pd.DataFrame(
        rows
    )


    result.to_csv(
        f"{OUTPUT_DIR}/yearly_return.csv",
        index=False
    )


    return result




# ======================================================
# 月度收益
# ======================================================

def generate_monthly_return(
    equity
):


    df=equity.copy()


    df["date"]=pd.to_datetime(
        df["date"]
    )


    df["month"]=(
        df["date"]
        .dt.to_period("M")
    )



    rows=[]


    for month,g in df.groupby(
        "month"
    ):

        start=(
            g["total_value"]
            .iloc[0]
        )

        end=(
            g["total_value"]
            .iloc[-1]
        )


        ret=(
            end/start-1
        )*100


        rows.append(
            {
                "month":
                    str(month),

                "return":
                    round(ret,2)

            }
        )


    result=pd.DataFrame(
        rows
    )


    result.to_csv(
        f"{OUTPUT_DIR}/monthly_return.csv",
        index=False
    )


    return result





# ======================================================
# 最大回撤曲线
# ======================================================

def generate_drawdown(
    equity
):


    df=equity.copy()


    df["date"]=pd.to_datetime(
        df["date"]
    )


    value=df["total_value"]


    high=value.cummax()


    df["drawdown"]=(
        value/high-1
    )*100



    df[
        [
            "date",
            "drawdown"
        ]
    ].to_csv(
        f"{OUTPUT_DIR}/drawdown.csv",
        index=False
    )



    return df




# ======================================================
# 主入口
# ======================================================

def main():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )


    equity=pd.read_csv(
        EQUITY_FILE
    )


    yearly=generate_yearly_return(
        equity
    )


    monthly=generate_monthly_return(
        equity
    )


    generate_drawdown(
        equity
    )


    print("="*60)

    print(
        "详细报告生成完成"
    )

    print("="*60)


    print()

    print(
        "年度收益:"
    )

    print(
        yearly.to_string(
            index=False
        )
    )



if __name__=="__main__":

    main()