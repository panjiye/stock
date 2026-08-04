from analysis.fundamental import fundamental_score



def combine_score(
    technical,
    fundamental
):


    return round(

        technical * 0.5

        +

        fundamental * 0.5

    ,2)





def score_stock(
    code,
    technical_score
):


    fundamental = fundamental_score(
        code
    )


    fund_score = fundamental["score"]


    total = combine_score(

        technical_score,

        fund_score

    )


    return {

        "code":code,

        "technical_score":technical_score,

        "fundamental_score":fund_score,

        "total_score":total,

        "fundamental_detail":
            fundamental["detail"]

    }