import os
import subprocess


ROOT = "."


IGNORE = {
    ".venv",
    ".git",
    "__pycache__",
    "archive",
}


def should_skip(path):
    parts = path.split(os.sep)

    return any(
        x in IGNORE
        for x in parts
    )


def main():

    errors = []

    for root, dirs, files in os.walk(ROOT):

        dirs[:] = [
            d for d in dirs
            if d not in IGNORE
        ]

        for file in files:

            if not file.endswith(".py"):
                continue

            path = os.path.join(
                root,
                file
            )

            if should_skip(path):
                continue


            module = (
                path
                .replace("./", "")
                .replace("/", ".")
                .replace(".py", "")
            )


            print(
                "=" * 70
            )

            print(
                "CHECK:",
                module
            )


            result = subprocess.run(
                [
                    "python",
                    "-c",
                    f"import {module}"
                ],
                capture_output=True,
                text=True
            )


            if result.returncode != 0:

                errors.append(
                    {
                        "module": module,
                        "error": result.stderr
                    }
                )

                print(
                    "FAILED"
                )

            else:

                print(
                    "OK"
                )


    print("\n\n")
    print("=" * 70)
    print(
        "IMPORT ERRORS:",
        len(errors)
    )
    print("=" * 70)


    for e in errors:

        print("\nMODULE:")
        print(
            e["module"]
        )

        print(
            e["error"]
        )


if __name__ == "__main__":
    main()

