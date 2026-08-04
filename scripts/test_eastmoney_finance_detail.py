import requests
import json


BASE = "https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/"


headers = {
    "User-Agent": "Mozilla/5.0"
}


tabs = [
    "lrb",
    "zcfzb",
    "xjllb"
]


for tab in tabs:

    print("\n====================")
    print(tab)

    url = BASE + tab + "AjaxNew"

    params = {
        "type": "0",
        "code": "SZ000001"
    }


    r = requests.get(
        url,
        params=params,
        headers=headers
    )


    print(r.url)

    print("status:", r.status_code)

    print(r.text[:300])

    try:
        data = r.json()

        print("JSON OK")

        print(data.keys())

        print(
            json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            )[:1000]
        )


    except Exception as e:

        print("不是JSON")
        print(e)