def calculate_equity(trades, initial_cash=100000):

    cash = initial_cash

    curve = []


    for t in trades:


        rate = t["return"] / 100


        cash = cash * (1 + rate)


        curve.append(
            {
                "date": t["sell_date"],
                "cash": round(cash,2)
            }
        )


    return curve

def calculate_drawdown(curve):


    max_cash = 0

    max_drawdown = 0


    for item in curve:


        cash = item["cash"]


        if cash > max_cash:

            max_cash = cash


        drawdown = (
            cash - max_cash
        ) / max_cash * 100


        if drawdown < max_drawdown:

            max_drawdown = drawdown



    return round(
        max_drawdown,
        2
    )

def find_max_drawdown_period(curve):


    peak_cash = 0
    peak_date = None

    max_dd = 0

    result = {}


    for item in curve:

        cash = item["cash"]
        date = item["date"]


        if cash > peak_cash:

            peak_cash = cash
            peak_date = date


        dd = (
            cash - peak_cash
        ) / peak_cash * 100


        if dd < max_dd:

            max_dd = dd

            result = {
                "start": peak_date,
                "end": date,
                "drawdown": round(dd,2)
            }


    return result