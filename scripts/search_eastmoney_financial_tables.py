import requests


headers = {

    "User-Agent":
    "Mozilla/5.0",

    "Referer":
    "https://data.eastmoney.com/"

}


url = "https://datacenter-web.eastmoney.com/api/data/v1/get"


# 常见财务报表关键词
keywords = [

    "BALANCE",
    "ASSET",
    "LIABILITY",
    "CASH",
    "FLOW",
    "FN",
    "FIN"

]


# 东方财富公开常用报表名空间
reports = [

    "RPT_FN_BALANCE",

    "RPT_FN_CASHFLOW",

    "RPT_FN_CASH_FLOW",

    "RPT_FN_BALANCE_SHEET",

    "RPT_FN_CASHFLOW_STATEMENT",

    "RPT_FCI_FN_BALANCE",

    "RPT_FCI_FN_CASHFLOW",

    "RPT_LICO_FN_CASHFLOW",

    "RPT_LICO_FN_BALANCE",

    "RPT_LICO_FN_BALANCE_DETAIL",

    "RPT_LICO_FN_CASHFLOW_DETAIL",

]


for report in reports:


    params={

        "reportName":report,

        "columns":"ALL",

        "filter":
        '(SECUCODE="000001.SZ")',

        "pageNumber":1,

        "pageSize":1

    }


    try:


        r=requests.get(

            url,

            params=params,

            headers=headers,

            timeout=10

        )


        j=r.json()


        print(
            report,
            "=>",
            j.get("success"),
            j.get("message")
        )


        if j.get("result"):

            print(
                j["result"]["data"][0].keys()
            )


    except Exception as e:

        print(
            report,
            e
        )