from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from .dataset import detect_delimiter, extract_all_tables_from_dir
from .schema import infer_table_schema


def load_relationships(data_dir: str | Path) -> list[dict[str, str]]:
    root = Path(data_dir)
    candidates = [
        root / 'Relationships.csv',
        root / 'relationships.csv',
        root / 'Relationships.tsv',
        root / 'relationships.tsv',
        root / 'SchemaMap.csv',
    ]
    rel_path = next((p for p in candidates if p.exists()), None)
    if not rel_path:
        return []

    with rel_path.open('r', newline='', encoding='utf-8-sig') as handle:
        delimiter = detect_delimiter(rel_path)
        reader = csv.DictReader(handle, delimiter=delimiter)
        raw_rows = [dict(row) for row in reader]

    normalized = []
    for r in raw_rows:
        from_table = r.get('FraTabell') or r.get('from_table') or r.get('source_table') or ''
        to_table = r.get('TilTabell') or r.get('to_table') or r.get('target_table') or ''
        from_col = r.get('FraKolonne') or r.get('from_column') or r.get('source_column') or ''
        to_col = r.get('TilKolonne') or r.get('to_column') or r.get('target_column') or ''
        if from_table and to_table:
            normalized.append({
                'FraTabell': from_table.strip(),
                'TilTabell': to_table.strip(),
                'FraKolonne': from_col.strip(),
                'TilKolonne': to_col.strip(),
            })
    return normalized


def discover_relationships(data_dir: str | Path) -> list[dict[str, str]]:
    """Skill 06: Discover Relationships - automatically infer foreign keys across entities."""
    root = Path(data_dir)
    tables = extract_all_tables_from_dir(root)
    discovered: list[dict[str, str]] = []

    # Map tables to column names (case-insensitive mapping)
    table_cols: dict[str, dict[str, str]] = {}
    for t_name, (header, _) in tables.items():
        if t_name.endswith('.csv'):
            continue  # Avoid duplicate alias
        table_cols[t_name] = {col.lower(): col for col in header}

    table_names = list(table_cols.keys())
    seen_pairs = set()

    for i in range(len(table_names)):
        t1 = table_names[i]
        cols1 = table_cols[t1]
        for j in range(i + 1, len(table_names)):
            t2 = table_names[j]
            cols2 = table_cols[t2]

            # Find matching identifier columns
            common_keys = set(cols1.keys()) & set(cols2.keys())
            for key in common_keys:
                # Prioritize ID, Code, Nr, Department, Project, Customer
                is_key = any(suffix in key for suffix in ('id', 'code', 'nr', 'key', 'department', 'wbs', 'konto', 'vessel'))
                if is_key:
                    pair_key = (min(t1, t2), max(t1, t2), key)
                    if pair_key not in seen_pairs:
                        seen_pairs.add(pair_key)
                        discovered.append({
                            'FraTabell': t1,
                            'TilTabell': t2,
                            'FraKolonne': cols1[key],
                            'TilKolonne': cols2[key],
                            'inferred': 'true',
                        })

    return discovered


def validate_relationships(data_dir: str | Path) -> dict[str, Any]:
    root = Path(data_dir)
    table_schemas = infer_table_schema(root)
    relationships = load_relationships(root)

    # If no explicit relationships file, auto-discover them (Skill 06)
    if not relationships:
        relationships = discover_relationships(root)

    issues: list[str] = []

    def _resolve_table(name: str) -> str | None:
        if name in table_schemas:
            return name
        if f"{name}.csv" in table_schemas:
            return f"{name}.csv"
        # Check without .csv
        clean_name = name[:-4] if name.endswith('.csv') else name
        if clean_name in table_schemas:
            return clean_name
        # Match case-insensitively
        for k in table_schemas:
            if k.lower() == name.lower() or k.lower() == f"{name.lower()}.csv":
                return k
        return None

    for relationship in relationships:
        from_table = relationship.get('FraTabell', '').strip()
        to_table = relationship.get('TilTabell', '').strip()
        from_column = relationship.get('FraKolonne', '').strip()
        to_column = relationship.get('TilKolonne', '').strip()

        resolved_from = _resolve_table(from_table)
        resolved_to = _resolve_table(to_table)

        if not resolved_from:
            issues.append(f'Missing source table: {from_table}')
            continue
        if not resolved_to:
            issues.append(f'Missing target table: {to_table}')
            continue

        cols_from = {c.lower(): c for c in table_schemas[resolved_from]}
        cols_to = {c.lower(): c for c in table_schemas[resolved_to]}

        if from_column.lower() not in cols_from:
            issues.append(f'Missing source column {from_table}.{from_column}')
        if to_column.lower() not in cols_to:
            issues.append(f'Missing target column {to_table}.{to_column}')

    return {
        'relationship_count': len(relationships),
        'valid': not issues,
        'issues': issues,
        'relationships': relationships,
    }
