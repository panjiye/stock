from pathlib import Path


ROOT = Path(".")


TARGETS = [
    "backtest",
    "scripts",
]


old = "from data.query"
new = "from data.query"


count = 0


for folder in TARGETS:

    for file in Path(folder).rglob("*.py"):

        text = file.read_text(
            encoding="utf-8"
        )


        if old in text:

            text = text.replace(
                old,
                new
            )

            file.write_text(
                text,
                encoding="utf-8"
            )

            print(
                "updated:",
                file
            )

            count += 1


print(
    f"\nTotal modified: {count}"
)