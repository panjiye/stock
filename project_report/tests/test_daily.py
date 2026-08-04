import baostock as bs

lg = bs.login()

print(lg.error_msg)

rs = bs.query_history_k_data_plus(
    "sh.600519",
    "date,open,high,low,close,volume",
    start_date="2025-01-01",
    end_date="2025-08-01",
    frequency="d"
)

while rs.next():
    print(rs.get_row_data())