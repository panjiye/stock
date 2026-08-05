# CHANGELOG


# V5-dev

日期：

2026-08-05


## 数据层迁移

完成：

- data/writer.py增强
- 建立统一写入层


迁移：

- download_index
- download_industry
- dividend downloader


新增：

- migrate_writer_v5.py
- migrate_dividend_writer_v5.py
- download_*_v5.py


## Git提交记录

主要提交：

- 5c68e57 migrate download_index
- 691bdb2 migrate download_industry
- 3b1e210 add dataframe upsert writer
- 268df88 migrate dividend downloader
- 9427bd0 add writer migration tools


---

# 下一阶段

继续迁移：

- profit downloader
- daily qfq downloader
- financial downloader
