import os
from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent


SCAN_DIRS = [
    ROOT / "scripts",
    ROOT / "data",
    ROOT / "analysis",
    ROOT / "backtest",
]


OUTPUT = ROOT / "reports" / "writer_migration_report.md"


KEYWORDS = [
    "sqlite3.connect",
    "sqlite3",
    "DB_PATH",
    "database/stock.db",
    "INSERT INTO",
    "INSERT OR IGNORE",
    "INSERT OR REPLACE",
    "cursor.execute",
    "conn.commit",
    "conn.close",
]


IGNORE_DIRS = {
    "__pycache__",
    ".venv",
    ".git",
}


def should_ignore(path):

    for part in path.parts:
        if part in IGNORE_DIRS:
            return True

    return False



def scan_file(path):

    result = []

    try:

        text = path.read_text(
            encoding="utf-8"
        )

    except Exception:

        return result


    for i,line in enumerate(
        text.splitlines(),
        1
    ):

        for key in KEYWORDS:

            if key in line:

                result.append(
                    {
                        "line": i,
                        "keyword": key,
                        "content": line.strip()
                    }
                )

    return result



def main():

    reports = []


    for scan_dir in SCAN_DIRS:

        if not scan_dir.exists():
            continue


        for path in scan_dir.rglob("*.py"):

            if should_ignore(path):
                continue


            result = scan_file(path)


            if result:

                reports.append(
                    (
                        path.relative_to(ROOT),
                        result
                    )
                )



    OUTPUT.parent.mkdir(
        exist_ok=True
    )


    with open(
        OUTPUT,
        "w",
        encoding="utf-8"
    ) as f:


        f.write(
            "# Writer Migration Report\n\n"
        )


        f.write(
            f"生成时间: {datetime.now()}\n\n"
        )


        f.write(
            "---\n\n"
        )


        for file,items in reports:


            f.write(
                f"## {file}\n\n"
            )


            for item in items:

                f.write(
                    f"- 行 {item['line']} "
                    f"`{item['keyword']}`\n"
                )

                f.write(
                    f"  ```python\n"
                    f"  {item['content']}\n"
                    f"  ```\n\n"
                )



    print(
        "=" * 60
    )

    print(
        "扫描完成"
    )

    print(
        f"发现文件: {len(reports)}"
    )

    print(
        f"报告: {OUTPUT}"
    )

    print(
        "=" * 60
    )



if __name__ == "__main__":

    main()
