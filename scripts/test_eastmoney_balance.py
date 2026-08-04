import requests


names = [

    "RPT_FCI_FN_BALANCE",
    "RPT_LICO_FN_BALANCE",
    "RPT_FN_BALANCE",
    "RPT_BALANCE_SHEET",
    "RPT_FCI_FN_BALANCE_NEW"

]


for name in names:


    url = (
        "https://datacenter-web.eastmoney.com/api/data/v1/get"
    )


    params={

        "reportName":name,

        "columns":"ALL",

        "filter":
        '(SECUCODE="000001.SZ")',

        "pageNumber":1,

        "pageSize":1

    }


    r=requests.get(
        url,
        params=params,
        timeout=10
    )


    data=r.json()


    print(
        "\n",
        name
    )

    print(
        data.get("success"),
        data.get("message")
    )