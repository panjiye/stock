import requests

url="https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/"

r=requests.get(
    url,
    params={
        "code":"SZ000001"
    },
    headers={
        "User-Agent":"Mozilla/5.0"
    }
)

print(r.status_code)

open(
    "/tmp/f10.html",
    "w",
    encoding="utf-8"
).write(r.text)

print("保存完成")