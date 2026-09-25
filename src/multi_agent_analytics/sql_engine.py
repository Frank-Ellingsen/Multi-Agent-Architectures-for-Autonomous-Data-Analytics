from __future__ import annotations

import csv
import sqlite3
from pathlib import Path
from typing import Any

from .dataset import detect_delimiter, stage_dataset_for_sql, SUPPORTED_EXTENSIONS

try:
    import duckdb  # type: ignore
    HAS_DUCKDB = True
except ImportError:
    HAS_DUCKDB = False


def execute_sql(data_dir: str | Path, query: str) -> list[dict[str, Any]]:
    """Executes analytical SQL across multi-format tables (CSV, TSV, Excel, PDF) in data_dir using DuckDB or SQLite."""
    root = Path(data_dir)
    # Ensure all multi-format files (Excel, TSV, PDF, etc.) are staged as queryable tables
    has_non_csv = any(
        f.suffix.lower() in SUPPORTED_EXTENSIONS and f.suffix.lower() != '.csv'
        for f in root.iterdir() if f.is_file()
    )
    if has_non_csv:
        stage_dataset_for_sql(root)

    if HAS_DUCKDB:
        return _execute_duckdb(root, query)
    return _execute_sqlite(root, query)


def _execute_duckdb(data_dir: Path, query: str) -> list[dict[str, Any]]:
    conn = duckdb.connect(database=':memory:')
    try:
        # Register raw CSV files
        for csv_file in data_dir.glob('*.csv'):
            table_name = csv_file.stem
            delimiter = detect_delimiter(csv_file)
            escaped_path = str(csv_file.resolve()).replace('\\', '/')
            conn.execute(
                f"CREATE VIEW IF NOT EXISTS \"{table_name}\" AS "
                f"SELECT * FROM read_csv_auto('{escaped_path}', delim='{delimiter}', header=True, ignore_errors=True)"
            )

        # Register staged tables (from Excel, PDF, TSV, PSV)
        staged_dir = data_dir / '.staged_cache'
        if staged_dir.exists():
            for csv_file in staged_dir.glob('*.csv'):
                table_name = csv_file.stem
                escaped_path = str(csv_file.resolve()).replace('\\', '/')
                conn.execute(
                    f"CREATE VIEW IF NOT EXISTS \"{table_name}\" AS "
                    f"SELECT * FROM read_csv_auto('{escaped_path}', delim=',', header=True, ignore_errors=True)"
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
        registered_tables = set()

        def _register_csv(csv_file: Path, delimiter: str):
            table_name = csv_file.stem
            if table_name in registered_tables:
                return
            with csv_file.open('r', encoding='utf-8-sig') as f:
                reader = csv.reader(f, delimiter=delimiter)
                headers = next(reader, None)
                if not headers:
                    return
                sanitized_cols = [f'"{col.strip()}" TEXT' for col in headers]
                conn.execute(f'CREATE TABLE "{table_name}" ({", ".join(sanitized_cols)})')
                placeholders = ', '.join(['?'] * len(headers))
                conn.executemany(f'INSERT INTO "{table_name}" VALUES ({placeholders})', reader)
                registered_tables.add(table_name)

        for csv_file in data_dir.glob('*.csv'):
            _register_csv(csv_file, detect_delimiter(csv_file))

        staged_dir = data_dir / '.staged_cache'
        if staged_dir.exists():
            for csv_file in staged_dir.glob('*.csv'):
                _register_csv(csv_file, ',')

        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()
