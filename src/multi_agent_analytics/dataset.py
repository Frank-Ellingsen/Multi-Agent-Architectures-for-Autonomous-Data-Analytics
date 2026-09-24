from __future__ import annotations

import csv
from pathlib import Path


def detect_delimiter(path: str | Path) -> str:
    sample_path = Path(path)
    with sample_path.open('r', newline='', encoding='utf-8-sig') as handle:
        sample = handle.read(4096)

    if not sample:
        return ';'

    candidates = [';', ',', '\t', '|']
    counts = {candidate: sample.count(candidate) for candidate in candidates}
    return max(candidates, key=lambda candidate: counts[candidate])


def load_dataset_summary(data_dir: str | Path) -> dict[str, dict[str, int | list[str]]]:
    root = Path(data_dir)
    summary: dict[str, dict[str, int | list[str]]] = {}

    for csv_path in sorted(root.glob('*.csv')):
        with csv_path.open('r', newline='', encoding='utf-8-sig') as handle:
            delimiter = detect_delimiter(csv_path)
            reader = csv.reader(handle, delimiter=delimiter)
            rows = list(reader)

        if not rows:
            summary[csv_path.name] = {'row_count': 0, 'column_count': 0, 'columns': []}
            continue

        header = rows[0]
        summary[csv_path.name] = {
            'row_count': len(rows) - 1,
            'column_count': len(header),
            'columns': header,
        }

    return summary
