#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
v5 writer migration helper

目标:
1. 扫描 dividend / stock download 相关脚本
2. 生成迁移报告
3. 不自动修改业务代码，避免破坏逻辑

说明:
第一次迁移不要自动替换大量代码。
先报告 -> 人工确认 -> 再覆盖。
"""

from pathlib import Path
from datetime import datetime


ROOT = Path(__file__).resolve().parent.parent

TARGET_FILES = [
    "scripts/download_dividend_all.py",
    "scripts/download_dividend_one.py",
    "scripts/download_one_stock.py",
]


REPORT = ROOT / "reports" / "dividend_writer_migration.md"


KEYWORDS = [
    "sqlite3.connect",
    "cursor.execute",
    "INSERT OR IGNORE",
    "INSERT OR REPLACE",
    "INSERT INTO",
    "conn.commit",
    "conn.close",
]


def scan_file(path):

    result = []

    if not path.exists():
        return result

    lines = path.read_text(
        encoding="utf-8"
    ).splitlines()


    for idx, line in enumerate(lines, 1):

        for key in KEYWORDS:

            if key in line:

                result.append(
                    {
                        "line": idx,
                        "keyword": key,
                        "content": line.strip()
                    }
                )

    return result



def main():

    REPORT.parent.mkdir(
        exist_ok=True
    )


    report = []

    report.append(
        "# Dividend Writer Migration Report\n"
    )

    report.append(
        f"生成时间: {datetime.now()}\n"
    )

    report.append(
        "---\n"
    )


    total = 0


    for filename in TARGET_FILES:

        path = ROOT / filename

        report.append(
            f"\n## {filename}\n"
        )


        findings = scan_file(path)


        if not findings:

            report.append(
                "无数据库写入痕迹\n"
            )

            continue


        for item in findings:

            total += 1

            report.append(
                f"""
- 行 {item['line']}
- 类型: `{item['keyword']}`

```python
{item['content']}
```
"""
            )


        report.append(
            "\n建议迁移:\n\n"
            "- sqlite3.connect -> data.query.engine\n"
            "- INSERT OR IGNORE -> data.writer.insert_ignore\n"
            "- INSERT OR REPLACE -> data.writer.insert_replace\n"
            "- 循环写入 -> dataframe 批量写入\n"
        )


    report.append(
        f"\n\n发现问题数量: {total}\n"
    )


    REPORT.write_text(
        "\n".join(report),
        encoding="utf-8"
    )


    print("=" * 60)
    print("扫描完成")
    print(f"报告: {REPORT}")
    print("=" * 60)



if __name__ == "__main__":
    main()