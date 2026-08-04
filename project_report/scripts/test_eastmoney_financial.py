import requests
import json


def test_financial(secid):

    url = (
        "https://datacenter-web.eastmoney.com/api/data/v1/get"
    )


    params = {

        "reportName":
        "RPT_LICO_FN_CPD",

        "columns":
        "ALL",

        "filter":
        f'(SECUCODE="{secid}")',

        "pageNumber":
        1,

        "pageSize":
        20,

    }


    r = requests.get(
        url,
        params=params,
        timeout=10
    )


    print(r.url)


    data = r.json()


    if not data.get("success"):

        print(data)

        return


    result = data["result"]


    print(
        "字段:"
    )

    print(
        list(
            result["data"][0].keys()
        )
    )


    print(
        "\n第一条数据:"
    )


    print(
        json.dumps(
            result["data"][0],
            indent=2,
            ensure_ascii=False
        )
    )



if __name__ == "__main__":

    test_financial(
        "000001.SZ"
    )