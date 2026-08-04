import requests


headers = {

    "User-Agent":
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36",

    "Referer":
    "https://data.eastmoney.com/"

}


url="https://datacenter-web.eastmoney.com/api/data/v1/get"


reports=[

"RPT_LICO_FN_CPD",

"RPT_FCI_FN_BALANCE",

"RPT_FCI_FN_CASHFLOW",

"RPT_FCI_FN_BALANCE_DETAIL",

"RPT_FCI_FN_CASHFLOW_DETAIL",

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


    r=requests.get(

        url,

        params=params,

        headers=headers,

        timeout=10

    )


    print("\n")

    print(report)

    print(r.url)


    try:

        j=r.json()

        print(
            j.get("success"),
            j.get("message")
        )


        if j.get("result"):

            print(
                "字段:",
                j["result"]["data"][0].keys()
            )


    except Exception as e:

        print(
            r.text[:200]
        )