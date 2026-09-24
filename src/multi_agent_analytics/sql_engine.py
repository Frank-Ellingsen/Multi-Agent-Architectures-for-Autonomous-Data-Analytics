from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Any

from .dataset import detect_delimiter

try:
    import duckdb  # type: ignore
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False


def execute_sql(data_dir: str | Path, query: str) -> list[dict[str, Any]]:
    """Executes analytical SQL across CSV files in data_dir using DuckDB, falling back to SQLite."""
    root = Path(data_dir)
    if HAS_DUCKDB:
        return _execute_duckdb(root, query)
    return _execute_sqlite(root, query)


def _execute_duckdb(data_dir: Path, query: str) -> list[dict[str, Any]]:
    conn = duckdb.connect(database=':memory:')
    try:
        # Register all CSV files as views/tables
        for csv_file in data_dir.glob('*.csv'):
            table_name = csv_file.stem
            delimiter = detect_delimiter(csv_file)
            escaped_path = str(csv_file.resolve()).replace('\\', '/')
            conn.execute(
                f"CREATE VIEW IF NOT EXISTS \"{table_name}\" AS "
                f"SELECT * FROM read_csv_auto('{escaped_path}', delim='{delimiter}', header=True, ignore_errors=True)"
            )
        cursor = conn.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    finally:
        conn.close()


def _execute_sqlite(data_dir: Path, query: str) -> list[dict[str, Any]]:
    conn = sqlite3.connect(':memory:')
    conn.row_factory = sqlite3.Row
    try:
        for csv_file in data_dir.glob('*.csv'):
            table_name = csv_file.stem
            delimiter = detect_delimiter(csv_file)
            with csv_file.open('r', encoding='utf-8-sig') as f:
                reader = csv.reader(f, delimiter=delimiter)
                headers = next(reader, None)
                if not headers:
                    continue
                sanitized_cols = [f'"{col.strip()}" TEXT' for col in headers]
                conn.execute(f'CREATE TABLE "{table_name}" ({", ".join(sanitized_cols)})')
                placeholders = ', '.join(['?'] * len(headers))
                conn.executemany(f'INSERT INTO "{table_name}" VALUES ({placeholders})', reader)

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
