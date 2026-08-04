import requests
import json


base = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/"


headers = {
    "User-Agent":
    "Mozilla/5.0",
    "Referer":
    "https://emweb.securities.eastmoney.com/"
}


apis = [
    "LRBAjaxNew",
    "ZCFZBAjaxNew",
    "XJLLBAjaxNew"
]


for api in apis:

    print("\n================")
    print(api)


    url = base + api


    params = {
        "type": "0",
        "code": "SZ000001",
        "pageIndex": "1",
        "pageSize": "50"
    }


    r = requests.get(
        url,
        params=params,
        headers=headers
    )


    print(r.url)
    print(r.status_code)

    print(r.text[:500])