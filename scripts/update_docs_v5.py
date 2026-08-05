"""
Update markdown docs for V5 data query migration.

Replace old query layer references:

analysis.query
analysis/query.py

to:

data.query
data/query.py

"""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


DOC_FILES = [
    "DATABASE.md",
    "FILE_CLEANUP_PLAN.md",
    "AI_DEVELOPMENT_PROTOCOL.md",
    "PROJECT_CONTEXT.md",
    "V5_MIGRATION_PLAN.md",
]


REPLACE_RULES = {
    "analysis.query": "data.query",
    "analysis/query.py": "data/query.py",
    "analysis\\query.py": "data\\query.py",
}


def update_file(path: Path):

    if not path.exists():
        print(f"skip missing: {path}")
        return


    text = path.read_text(
        encoding="utf-8"
    )


    old = text


    for src, dst in REPLACE_RULES.items():
        text = text.replace(
            src,
            dst
        )


    if text != old:

        path.write_text(
            text,
            encoding="utf-8"
        )

        print(
            f"updated: {path.relative_to(ROOT)}"
        )

    else:

        print(
            f"unchanged: {path.relative_to(ROOT)}"
        )



def main():

    count = 0


    for filename in DOC_FILES:

        file = ROOT / filename

        before = file.read_text(
            encoding="utf-8"
        ) if file.exists() else ""


        update_file(file)


        after = file.read_text(
            encoding="utf-8"
        ) if file.exists() else ""


        if before != after:
            count += 1


    print()
    print(
        f"Modified documents: {count}"
    )



if __name__ == "__main__":
    main()
