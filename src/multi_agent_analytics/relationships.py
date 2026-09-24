from __future__ import annotations

import csv
from pathlib import Path

from .dataset import detect_delimiter
from .schema import infer_table_schema


def load_relationships(data_dir: str | Path) -> list[dict[str, str]]:
    root = Path(data_dir)
    relationships_path = root / 'Relationships.csv'
    if not relationships_path.exists():
        return []

    with relationships_path.open('r', newline='', encoding='utf-8-sig') as handle:
        delimiter = detect_delimiter(relationships_path)
        reader = csv.DictReader(handle, delimiter=delimiter)
        return [dict(row) for row in reader]


def validate_relationships(data_dir: str | Path) -> dict[str, object]:
    root = Path(data_dir)
    table_schemas = infer_table_schema(root)
    relationships = load_relationships(root)
    issues: list[str] = []

    for relationship in relationships:
        from_table = relationship.get('FraTabell', '').strip()
        to_table = relationship.get('TilTabell', '').strip()
        from_column = relationship.get('FraKolonne', '').strip()
        to_column = relationship.get('TilKolonne', '').strip()

        from_file = f'{from_table}.csv'
        to_file = f'{to_table}.csv'

        if from_file not in table_schemas:
            issues.append(f'Missing source table: {from_file}')
            continue
        if to_file not in table_schemas:
            issues.append(f'Missing target table: {to_file}')
            continue

        if from_column not in table_schemas[from_file]:
            issues.append(f'Missing source column {from_table}.{from_column}')
        if to_column not in table_schemas[to_file]:
            issues.append(f'Missing target column {to_table}.{to_column}')

    return {
        'relationship_count': len(relationships),
        'valid': not issues,
        'issues': issues,
    }
