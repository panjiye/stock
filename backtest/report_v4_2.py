import pandas as pd
import os

from data.query import engine

from backtest.advanced_metrics import (
    calculate_alpha_beta,
    calculate_excess_return,
    calculate_drawdown_period,
    yearly_return,
    monthly_return
)


EQUITY_FILE = (
    "results_v4_2/equity.csv"
)


# =====================================================
# 读取指数
# =====================================================

def load_benchmark(
    code="000300.SH"
):

    conn = engine.connect(
        DB_PATH
    )


    df = pd.read_sql(
        f"""
        select
            date,
            close as value
        from index_price
        where code='{code}'
        order by date
        """,

        conn
    )


    conn.close()


    df["date"] = pd.to_datetime(
        df["date"]
    )


    return df

# =====================================================
# 基础指标
# =====================================================

def basic_report(
    equity
):


    # start = (
    #     equity["total_value"]
    #     .iloc[0]
    # )

    INITIAL_CAPITAL = 1000000

    start = INITIAL_CAPITAL

    end = (
        equity["total_value"]
        .iloc[-1]
    )


    total_return = (
        end/start-1
    )*100



    years = (

        pd.to_datetime(
            equity["date"].iloc[-1]
        )

        -

        pd.to_datetime(
            equity["date"].iloc[0]
        )

    ).days / 365



    annual = (
        (end/start)
        **
        (1/years)
        -
        1
    )*100



    return {

        "initial":
            start,

        "final":
            end,

        "total":
            total_return,

        "annual":
            annual

    }





# =====================================================
# 主报告
# =====================================================

def generate_report():


    print("="*60)

    print(
        "量化回测报告"
    )

    print("="*60)



    equity=pd.read_csv(
        EQUITY_FILE
    )



    equity["date"]=pd.to_datetime(
        equity["date"]
    )



    result=basic_report(
        equity
    )



    print()

    print(
        "资金:"
    )

    print(
        f"初始资金: {result['initial']:,.2f}"
    )

    print(
        f"最终资产: {result['final']:,.2f}"
    )

    print(
        f"累计收益: {result['total']:.2f}%"
    )

    print(
        f"年化收益: {result['annual']:.2f}%"
    )



    print()

    print(
        "="*60
    )

    print(
        "风险归因"
    )

    print(
        "="*60
    )



    benchmark = load_benchmark()


    benchmark = benchmark[
        benchmark["date"]
        >=
        equity["date"].iloc[0]
    ]



    ab = calculate_alpha_beta(
        equity,
        benchmark
    )


    print(
        "Alpha:",
        ab["alpha"],
        "%"
    )


    print(
        "Beta:",
        ab["beta"]
    )



    dd = calculate_drawdown_period(
        equity,
        "total_value"
    )



    print()

    print(
        "最大回撤:"
    )

    print(
        dd
    )



    print()

    print(
        "="*60
    )

    print(
        "生成分析文件"
    )

    print(
        "="*60
    )



    os.makedirs(
        "results_v4_2",
        exist_ok=True
    )



    # 超额收益

    excess = calculate_excess_return(
        equity,
        benchmark
    )


    excess.to_csv(
        "results_v4_2/excess_return.csv",
        index=False
    )



    # 年收益

    yearly = yearly_return(
        equity,
        "total_value"
    )


    yearly.to_csv(
        "results_v4_2/yearly_return.csv",
        index=False
    )



    # 月收益

    monthly = monthly_return(
        equity,
        "total_value"
    )


    monthly.to_csv(
        "results_v4_2/monthly_return.csv",
        index=False
    )



    print(
        "完成"
    )





if __name__=="__main__":

    generate_report()