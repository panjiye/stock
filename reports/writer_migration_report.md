# Writer Migration Report

生成时间: 2026-08-05 13:33:18.364123

---

## scripts/migrate_sqlite_to_engine_v5.py

- 行 8 `sqlite3.connect`
  ```python
  sqlite3.connect(DB_PATH)
  ```

- 行 8 `sqlite3`
  ```python
  sqlite3.connect(DB_PATH)
  ```

- 行 8 `DB_PATH`
  ```python
  sqlite3.connect(DB_PATH)
  ```

- 行 14 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 16 `DB_PATH`
  ```python
  DB_PATH = "database/stock.db"
  ```

- 行 16 `database/stock.db`
  ```python
  DB_PATH = "database/stock.db"
  ```

- 行 74 `sqlite3`
  ```python
  "import sqlite3\n",
  ```

- 行 80 `DB_PATH`
  ```python
  # remove DB_PATH definitions
  ```

- 行 94 `DB_PATH`
  ```python
  "DB_PATH = "
  ```

- 行 110 `sqlite3.connect`
  ```python
  "sqlite3.connect(",
  ```

- 行 110 `sqlite3`
  ```python
  "sqlite3.connect(",
  ```

## scripts/fix_daily_price.py

- 行 1 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 4 `database/stock.db`
  ```python
  db = "database/stock.db"
  ```

- 行 8 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(db)
  ```

- 行 8 `sqlite3`
  ```python
  conn = sqlite3.connect(db)
  ```

- 行 14 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 29 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 30 `INSERT INTO`
  ```python
  INSERT INTO daily_price_new
  ```

- 行 45 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 51 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 58 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 64 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 66 `conn.close`
  ```python
  conn.close()
  ```

## scripts/migrate_writer_v5.py

- 行 21 `sqlite3.connect`
  ```python
  "sqlite3.connect",
  ```

- 行 21 `sqlite3`
  ```python
  "sqlite3.connect",
  ```

- 行 22 `sqlite3`
  ```python
  "sqlite3",
  ```

- 行 23 `DB_PATH`
  ```python
  "DB_PATH",
  ```

- 行 24 `database/stock.db`
  ```python
  "database/stock.db",
  ```

- 行 25 `INSERT INTO`
  ```python
  "INSERT INTO",
  ```

- 行 26 `INSERT OR IGNORE`
  ```python
  "INSERT OR IGNORE",
  ```

- 行 27 `INSERT OR REPLACE`
  ```python
  "INSERT OR REPLACE",
  ```

- 行 28 `cursor.execute`
  ```python
  "cursor.execute",
  ```

- 行 29 `conn.commit`
  ```python
  "conn.commit",
  ```

- 行 30 `conn.close`
  ```python
  "conn.close",
  ```

## scripts/download_dividend_all.py

- 行 1 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 6 `database/stock.db`
  ```python
  DB = "database/stock.db"
  ```

- 行 10 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 10 `sqlite3`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 14 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 15 `INSERT OR REPLACE`
  ```python
  INSERT OR REPLACE INTO download_log
  ```

- 行 38 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 39 `conn.close`
  ```python
  conn.close()
  ```

- 行 61 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 61 `sqlite3`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 65 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 66 `INSERT OR IGNORE`
  ```python
  INSERT OR IGNORE INTO dividend
  ```

- 行 85 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 86 `conn.close`
  ```python
  conn.close()
  ```

- 行 157 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 157 `sqlite3`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 162 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 178 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 198 `conn.close`
  ```python
  conn.close()
  ```

## scripts/create_tables.py

- 行 1 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 2 `database/stock.db`
  ```python
  db = "database/stock.db"
  ```

- 行 7 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(db)
  ```

- 行 7 `sqlite3`
  ```python
  conn = sqlite3.connect(db)
  ```

- 行 16 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 43 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 70 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 97 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 116 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 152 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 191 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 199 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 224 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 232 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 260 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 268 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 298 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 306 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 308 `conn.close`
  ```python
  conn.close()
  ```

## scripts/download_one_stock.py

- 行 3 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 35 `INSERT INTO`
  ```python
  INSERT INTO download_log
  ```

- 行 58 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(db_file)
  ```

- 行 58 `sqlite3`
  ```python
  conn = sqlite3.connect(db_file)
  ```

- 行 62 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 75 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 77 `conn.close`
  ```python
  conn.close()
  ```

## scripts/download_daily_qfq_all.py

- 行 1 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 129 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(
  ```

- 行 129 `sqlite3`
  ```python
  conn = sqlite3.connect(
  ```

- 行 138 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 140 `INSERT OR REPLACE`
  ```python
  INSERT OR REPLACE INTO download_log
  ```

- 行 163 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 165 `conn.close`
  ```python
  conn.close()
  ```

- 行 178 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(
  ```

- 行 178 `sqlite3`
  ```python
  conn = sqlite3.connect(
  ```

- 行 187 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 201 `conn.close`
  ```python
  conn.close()
  ```

- 行 363 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 363 `sqlite3`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 368 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 383 `conn.close`
  ```python
  conn.close()
  ```

## scripts/download_financial_all_v2.py

- 行 1 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 6 `DB_PATH`
  ```python
  DB_PATH = "database/stock.db"
  ```

- 行 6 `database/stock.db`
  ```python
  DB_PATH = "database/stock.db"
  ```

- 行 35 `sqlite3.connect`
  ```python
  return sqlite3.connect(DB_PATH)
  ```

- 行 35 `sqlite3`
  ```python
  return sqlite3.connect(DB_PATH)
  ```

- 行 35 `DB_PATH`
  ```python
  return sqlite3.connect(DB_PATH)
  ```

- 行 85 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 86 `conn.close`
  ```python
  conn.close()
  ```

- 行 109 `conn.close`
  ```python
  conn.close()
  ```

- 行 143 `conn.close`
  ```python
  conn.close()
  ```

- 行 389 `INSERT OR IGNORE`
  ```python
  INSERT OR IGNORE INTO financial_profit
  ```

- 行 431 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 433 `conn.close`
  ```python
  conn.close()
  ```

## scripts/download_industry_v3.py

- 行 13 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 17 `DB_PATH`
  ```python
  #from data.query import DB_PATH
  ```

- 行 39 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(
  ```

- 行 39 `sqlite3`
  ```python
  conn = sqlite3.connect(
  ```

- 行 100 `INSERT OR REPLACE`
  ```python
  INSERT OR REPLACE INTO stock_industry
  ```

- 行 131 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 133 `conn.close`
  ```python
  conn.close()
  ```

## scripts/download_dividend_one.py

- 行 1 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 6 `database/stock.db`
  ```python
  DB = "database/stock.db"
  ```

- 行 11 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 11 `sqlite3`
  ```python
  conn = sqlite3.connect(DB)
  ```

- 行 15 `cursor.execute`
  ```python
  cursor.execute("""
  ```

- 行 16 `INSERT OR IGNORE`
  ```python
  INSERT OR IGNORE INTO dividend
  ```

- 行 38 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 39 `conn.close`
  ```python
  conn.close()
  ```

## scripts/download_all_daily.py

- 行 1 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 22 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(db)
  ```

- 行 22 `sqlite3`
  ```python
  conn = sqlite3.connect(db)
  ```

- 行 31 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 49 `conn.close`
  ```python
  conn.close()
  ```

## scripts/download_profit_all.py

- 行 2 `sqlite3`
  ```python
  import sqlite3
  ```

- 行 13 `database/stock.db`
  ```python
  DB = "database/stock.db"
  ```

- 行 31 `sqlite3.connect`
  ```python
  conn = sqlite3.connect(
  ```

- 行 31 `sqlite3`
  ```python
  conn = sqlite3.connect(
  ```

- 行 96 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 246 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 248 `INSERT OR REPLACE`
  ```python
  INSERT OR REPLACE INTO download_log
  ```

- 行 283 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 511 `cursor.execute`
  ```python
  cursor.execute(
  ```

- 行 515 `INSERT OR IGNORE`
  ```python
  INSERT OR IGNORE INTO financial_profit
  ```

- 行 588 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 614 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 667 `conn.commit`
  ```python
  conn.commit()
  ```

- 行 735 `conn.close`
  ```python
  conn.close()
  ```

## data/query.py

- 行 46 `DB_PATH`
  ```python
  DB_PATH = DB_FILE
  ```

## data/writer.py

- 行 101 `INSERT OR IGNORE`
  ```python
  INSERT OR IGNORE INTO {table}
  ```

- 行 136 `INSERT OR REPLACE`
  ```python
  sqlite INSERT OR REPLACE 替代方案
  ```

- 行 174 `INSERT INTO`
  ```python
  INSERT INTO {table}
  ```

## analysis/fundamental.py

- 行 37 `conn.close`
  ```python
  conn.close()
  ```

- 行 98 `conn.close`
  ```python
  conn.close()
  ```

- 行 165 `conn.close`
  ```python
  conn.close()
  ```

## backtest/drawdown_industry_analysis_v4.py

- 行 109 `DB_PATH`
  ```python
  DB_PATH
  ```

- 行 123 `conn.close`
  ```python
  conn.close()
  ```

## backtest/report.py

- 行 29 `DB_PATH`
  ```python
  DB_PATH
  ```

- 行 47 `conn.close`
  ```python
  conn.close()
  ```

## backtest/drawdown_analysis_v2.py

- 行 59 `DB_PATH`
  ```python
  DB_PATH
  ```

- 行 73 `conn.close`
  ```python
  conn.close()
  ```

## backtest/report_chart.py

- 行 53 `DB_PATH`
  ```python
  DB_PATH
  ```

- 行 70 `conn.close`
  ```python
  conn.close()
  ```

## backtest/risk_overlay_test.py

- 行 15 `DB_PATH`
  ```python
  conn = engine.connect(DB_PATH)
  ```

- 行 29 `conn.close`
  ```python
  conn.close()
  ```

## backtest/drawdown_contribution_v2.py

- 行 67 `DB_PATH`
  ```python
  DB_PATH
  ```

- 行 81 `conn.close`
  ```python
  conn.close()
  ```

## backtest/benchmark.py

- 行 192 `conn.close`
  ```python
  conn.close()
  ```

## backtest/report_v4_2.py

- 行 29 `DB_PATH`
  ```python
  DB_PATH
  ```

- 行 47 `conn.close`
  ```python
  conn.close()
  ```

## backtest/risk_v2.py

- 行 50 `conn.close`
  ```python
  conn.close()
  ```

## backtest/risk_overlay_simulation.py

- 行 39 `DB_PATH`
  ```python
  conn = engine.connect(DB_PATH)
  ```

- 行 53 `conn.close`
  ```python
  conn.close()
  ```

## backtest/drawdown_analysis.py

- 行 90 `DB_PATH`
  ```python
  DB_PATH
  ```

- 行 105 `conn.close`
  ```python
  conn.close()
  ```

## backtest/drawdown_industry_analysis.py

- 行 30 `DB_PATH`
  ```python
  conn = engine.connect(DB_PATH)
  ```

- 行 42 `conn.close`
  ```python
  conn.close()
  ```

## backtest/drawdown_contribution.py

- 行 63 `DB_PATH`
  ```python
  DB_PATH
  ```

- 行 77 `conn.close`
  ```python
  conn.close()
  ```

