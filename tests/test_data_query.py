from data.query import (
    get_stock_daily,
    get_stock_list,
    get_latest_price,
    get_index_daily,
)


def test_stock_daily():

    df = get_stock_daily(
        "600519"
    )

    print(df.head())

    assert len(df) > 0



def test_stock_list():

    df = get_stock_list()

    print(df.head())

    assert len(df) > 0



def test_latest_price():

    df = get_latest_price()

    print(df.head())

    assert len(df) > 0



def test_index_daily():

    df = get_index_daily(
        "000300"
    )

    print(df.head())

    assert len(df) > 0
