def calculate_score(df):

    """
    技术评分

    返回:
    总分
    评分明细
    """

    detail = {

        "RSI":0,
        "MA趋势":0,
        "MACD":0,
        "KDJ":0

    }


    latest = df.iloc[-1]

    yesterday = df.iloc[-2]


    # RSI

    rsi = latest["RSI"]


    if 60 <= rsi <= 70:

        detail["RSI"] = 15

    elif 50 <= rsi < 60:

        detail["RSI"] = 10

    elif rsi > 70:

        detail["RSI"] = 5



    # MA趋势

    if latest["close"] > latest["MA20"]:

        detail["MA趋势"] += 15


    if latest["MA20"] > latest["MA60"]:

        detail["MA趋势"] += 15



    # MACD

    if latest["MACD"] > 0:

        detail["MACD"] += 10


    if latest["MACD"] > yesterday["MACD"]:

        detail["MACD"] += 10



    # KDJ

    if latest["K"] > latest["D"]:

        detail["KDJ"] += 10


    if latest["J"] > 80:

        detail["KDJ"] += 5



    return sum(detail.values()), detail