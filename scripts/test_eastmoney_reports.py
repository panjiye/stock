import requests
import json


url = (
    "https://datacenter-web.eastmoney.com/api/data/v1/get"
)


params = {

    "reportName":
    "RPT_FCI_FN_CPD",

    "columns":
    "ALL",

    "filter":
    '(SECUCODE="000001.SZ")',

    "pageNumber":
    1,

    "pageSize":
    1

}


r=requests.get(
    url,
    params=params,
    timeout=10
)


data=r.json()


print(
    json.dumps(
        data,
        indent=2,
        ensure_ascii=False
    )
)