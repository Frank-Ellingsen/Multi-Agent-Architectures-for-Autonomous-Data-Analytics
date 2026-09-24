from __future__ import annotations

import csv
from pathlib import Path

from .dataset import detect_delimiter


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
    cleaned = [value.strip() for value in values if str(value).strip()]
    if not cleaned:
        return 'unknown'

    int_count = 0
    float_count = 0
    bool_count = 0
    for value in cleaned:
        lowered = value.lower()
        if lowered in {'true', 'false', 'ja', 'nei', 'yes', 'no'}:
            bool_count += 1
            continue
        try:
            int(value)
            int_count += 1
            continue
        except ValueError:
            pass
        if _normalize_numeric(value) is not None:
            float_count += 1

    if bool_count == len(cleaned):
        return 'boolean'
    if int_count == len(cleaned):
        return 'integer'
    if float_count == len(cleaned):
        return 'float'

    return 'string'


def infer_table_schema(data_dir: str | Path) -> dict[str, dict[str, str]]:
    root = Path(data_dir)
    schemas: dict[str, dict[str, str]] = {}

    for csv_path in sorted(root.glob('*.csv')):
        with csv_path.open('r', newline='', encoding='utf-8-sig') as handle:
            delimiter = detect_delimiter(csv_path)
            reader = csv.reader(handle, delimiter=delimiter)
            rows = list(reader)

        if not rows:
            schemas[csv_path.name] = {}
            continue

        header = rows[0]
        sample_values = {column: [] for column in header}
        for row in rows[1:]:
            for index, column in enumerate(header):
                if index < len(row):
                    sample_values[column].append(row[index])

        column_types = {column: infer_type(sample_values[column]) for column in header}
        schemas[csv_path.name] = column_types

    return schemas


def summarize_schema(data_dir: str | Path) -> dict[str, dict[str, str]]:
    return infer_table_schema(data_dir)
