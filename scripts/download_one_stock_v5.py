from datetime import datetime

from data.writer import execute_sql


def save_log(code, data_type, status, message):

    sql = """
    INSERT OR REPLACE INTO download_log
    (
        code,
        data_type,
        status,
        message,
        update_time
    )
    VALUES
    (
        :code,:data_type,:status,:message,:update_time
    )
    """

    execute_sql(
        sql,
        {
            "code": code,
            "data_type": data_type,
            "status": status,
            "message": message,
            "update_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )


def main():

    print("download_one_stock v5 writer layer ready")


if __name__ == "__main__":
    main()
