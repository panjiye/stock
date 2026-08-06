import pandas as pd
import matplotlib.pyplot as plt



def main():


    print("="*60)

    print(
        "绘制净值曲线"
    )


    cost=pd.read_csv(
        "backtest_equity_cost.csv"
    )


    cost["date"]=pd.to_datetime(
        cost["sell_date"]
    )


    cost["strategy"]=(
        cost["value"]
        /
        cost["value"].iloc[0]
    )



    plt.figure(
        figsize=(12,6)
    )


    plt.plot(

        cost["date"],

        cost["strategy"],

        label="Strategy"

    )


    try:


        benchmark=pd.read_csv(
            "benchmark.csv"
        )


        benchmark["date"]=pd.to_datetime(
            benchmark["date"]
        )


        plt.plot(

            benchmark["date"],

            benchmark["benchmark"],

            label="CSI300"

        )


    except:


        print(
            "没有benchmark数据"
        )



    plt.title(
        "Factor Strategy vs Benchmark"
    )


    plt.xlabel(
        "Date"
    )


    plt.ylabel(
        "Net Value"
    )


    plt.legend()


    plt.grid()



    plt.savefig(

        "backtest_curve.png",

        dpi=300,

        bbox_inches="tight"

    )


    print(
        "图片生成:"
    )


    print(
        "backtest_curve.png"
    )



if __name__=="__main__":

    main()