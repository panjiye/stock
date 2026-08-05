# Dividend Writer Migration Report

生成时间: 2026-08-05 13:42:51.836035

---


## scripts/download_dividend_all.py


- 行 10
- 类型: `sqlite3.connect`

```python
conn = sqlite3.connect(DB)
```


- 行 14
- 类型: `cursor.execute`

```python
cursor.execute("""
```


- 行 15
- 类型: `INSERT OR REPLACE`

```python
INSERT OR REPLACE INTO download_log
```


- 行 38
- 类型: `conn.commit`

```python
conn.commit()
```


- 行 39
- 类型: `conn.close`

```python
conn.close()
```


- 行 61
- 类型: `sqlite3.connect`

```python
conn = sqlite3.connect(DB)
```


- 行 65
- 类型: `cursor.execute`

```python
cursor.execute("""
```


- 行 66
- 类型: `INSERT OR IGNORE`

```python
INSERT OR IGNORE INTO dividend
```


- 行 85
- 类型: `conn.commit`

```python
conn.commit()
```


- 行 86
- 类型: `conn.close`

```python
conn.close()
```


- 行 157
- 类型: `sqlite3.connect`

```python
conn = sqlite3.connect(DB)
```


- 行 162
- 类型: `cursor.execute`

```python
cursor.execute("""
```


- 行 178
- 类型: `cursor.execute`

```python
cursor.execute("""
```


- 行 198
- 类型: `conn.close`

```python
conn.close()
```


建议迁移:

- sqlite3.connect -> data.query.engine
- INSERT OR IGNORE -> data.writer.insert_ignore
- INSERT OR REPLACE -> data.writer.insert_replace
- 循环写入 -> dataframe 批量写入


## scripts/download_dividend_one.py


- 行 11
- 类型: `sqlite3.connect`

```python
conn = sqlite3.connect(DB)
```


- 行 15
- 类型: `cursor.execute`

```python
cursor.execute("""
```


- 行 16
- 类型: `INSERT OR IGNORE`

```python
INSERT OR IGNORE INTO dividend
```


- 行 38
- 类型: `conn.commit`

```python
conn.commit()
```


- 行 39
- 类型: `conn.close`

```python
conn.close()
```


建议迁移:

- sqlite3.connect -> data.query.engine
- INSERT OR IGNORE -> data.writer.insert_ignore
- INSERT OR REPLACE -> data.writer.insert_replace
- 循环写入 -> dataframe 批量写入


## scripts/download_one_stock.py


- 行 35
- 类型: `INSERT INTO`

```python
INSERT INTO download_log
```


- 行 58
- 类型: `sqlite3.connect`

```python
conn = sqlite3.connect(db_file)
```


- 行 62
- 类型: `cursor.execute`

```python
cursor.execute(
```


- 行 75
- 类型: `conn.commit`

```python
conn.commit()
```


- 行 77
- 类型: `conn.close`

```python
conn.close()
```


建议迁移:

- sqlite3.connect -> data.query.engine
- INSERT OR IGNORE -> data.writer.insert_ignore
- INSERT OR REPLACE -> data.writer.insert_replace
- 循环写入 -> dataframe 批量写入



发现问题数量: 24
