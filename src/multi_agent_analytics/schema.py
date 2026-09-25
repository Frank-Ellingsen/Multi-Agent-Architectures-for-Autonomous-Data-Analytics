from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .dataset import extract_all_tables_from_dir


def _normalize_numeric(value: str) -> float | None:
    if value is None:
        return None
    text = str(value).strip()
    if not text:
        return None
    text = text.replace(' ', '')
    if text.lower() in {'null', 'none', 'n/a', 'na'}:
        return None
    try:
        if '.' in text and ',' in text:
            text = text.replace('.', '').replace(',', '.')
        elif ',' in text:
            text = text.replace(',', '.')
        return float(text)
    except ValueError:
        return None


def infer_type(values: list[str]) -> str:
    cleaned = [str(value).strip() for value in values if str(value).strip()]
    if not cleaned:
        return 'string'

    int_count = 0
    float_count = 0
    bool_count = 0
    date_count = 0

    date_pattern = re.compile(r'^\d{4}[-/]\d{2}[-/]\d{2}$|^\d{2}[-/]\d{2}[-/]\d{4}$')

    for value in cleaned:
        lowered = value.lower()
        if lowered in {'true', 'false', 'ja', 'nei', 'yes', 'no'}:
            bool_count += 1
            continue
        if date_pattern.match(value):
            date_count += 1
            continue
        try:
            int(value)
            int_count += 1
            continue
        except ValueError:
            pass
        if _normalize_numeric(value) is not None:
            float_count += 1

    total = len(cleaned)
    if bool_count == total:
        return 'boolean'
    if int_count == total:
        return 'integer'
    if (int_count + float_count) == total:
        return 'float'

    return 'string'


def infer_table_schema(data_dir: str | Path) -> dict[str, dict[str, str]]:
    root = Path(data_dir)
    schemas: dict[str, dict[str, str]] = {}
    tables = extract_all_tables_from_dir(root)

    for table_name, (header, rows) in tables.items():
        if not header:
            schemas[table_name] = {}
            continue

        sample_values: dict[str, list[str]] = {column: [] for column in header}
        for row in rows[:500]:
            for index, column in enumerate(header):
                if index < len(row):
                    sample_values[column].append(row[index])

        column_types = {column: infer_type(sample_values[column]) for column in header}
        schemas[table_name] = column_types

    return schemas


def summarize_schema(data_dir: str | Path) -> dict[str, dict[str, str]]:
    return infer_table_schema(data_dir)
