"""
V5 SQLite -> data.query.engine migration tool

用途:
批量迁移分析/回测模块数据库访问方式

修改:
sqlite3.connect(DB_PATH)
        |
        v
engine.connect()

删除:
import sqlite3

DB_PATH = "database/stock.db"

增加:
from data.query import engine


默认处理:
analysis/
backtest/
tools/

不会处理:
scripts/
tests/

原因:
scripts 可能包含数据库写入逻辑
tests 可能依赖 sqlite 行为
"""

import os


ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


TARGET_DIRS = [
    "backtest",
    "tools",
]


def migrate_file(path):

    if not path.endswith(".py"):
        return False


    with open(
        path,
        "r",
        encoding="utf-8"
    ) as f:
        content = f.read()


    original = content


    # --------------------------
    # sqlite import
    # --------------------------

    content = content.replace(
        "import sqlite3\n",
        ""
    )


    # --------------------------
    # remove DB_PATH definitions
    # --------------------------

    lines = content.splitlines()


    new_lines = []

    skip = False


    for line in lines:

        if line.startswith(
            "DB_PATH = "
        ):
            continue


        new_lines.append(line)


    content = "\n".join(new_lines)


    # --------------------------
    # connect migration
    # --------------------------

    content = content.replace(
        "sqlite3.connect(",
        "engine.connect("
    )


    # --------------------------
    # add engine import
    # --------------------------

    if (
        "engine.connect(" in content
        and
        "from data.query import engine" not in content
    ):

        lines = content.splitlines()

        insert_pos = 0

        for i, line in enumerate(lines):

            if (
                line.startswith("import ")
                or
                line.startswith("from ")
            ):
                insert_pos = i + 1


        lines.insert(
            insert_pos,
            "from data.query import engine"
        )


        content = "\n".join(lines)



    if content != original:

        with open(
            path,
            "w",
            encoding="utf-8"
        ) as f:
            f.write(content)

        print(
            "updated:",
            os.path.relpath(path, ROOT)
        )

        return True


    return False



def main():

    count = 0


    for folder in TARGET_DIRS:

        folder_path = os.path.join(
            ROOT,
            folder
        )


        if not os.path.exists(folder_path):
            continue


        for root, dirs, files in os.walk(folder_path):

            if "__pycache__" in root:
                continue


            for file in files:

                if file.endswith(".py"):

                    path = os.path.join(
                        root,
                        file
                    )

                    if migrate_file(path):
                        count += 1


    print()
    print("=" * 60)
    print(
        "Modified files:",
        count
    )
    print("=" * 60)



if __name__ == "__main__":
    main()

