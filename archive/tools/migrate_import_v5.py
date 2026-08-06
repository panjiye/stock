#!/usr/bin/env python3
"""
V5 Import Migration Tool

自动迁移：

analysis.query
        |
        v
data.query


"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


TARGET_FILES = [
    "py"
]


EXCLUDE_DIRS = {
    ".venv",
    ".git",
    "archive",
    "database",
    "__pycache__",
    "results"
}



OLD = "from data.query"
NEW = "from data.query"



def should_skip(path):

    for part in path.parts:
        if part in EXCLUDE_DIRS:
            return True

    return False



def migrate_file(path):

    text = path.read_text(
        encoding="utf-8"
    )

    if OLD not in text:
        return False


    new_text = text.replace(
        OLD,
        NEW
    )


    path.write_text(
        new_text,
        encoding="utf-8"
    )


    print(
        f"migrated: {path}"
    )

    return True



def main():

    count = 0


    for path in ROOT.rglob("*.py"):

        if should_skip(path):
            continue


        if migrate_file(path):
            count += 1


    print()
    print(
        f"total migrated: {count}"
    )



if __name__ == "__main__":
    main()