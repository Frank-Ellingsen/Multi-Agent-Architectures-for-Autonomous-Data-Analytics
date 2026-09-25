from __future__ import annotations

import csv
import datetime
from pathlib import Path
from typing import Any

SUPPORTED_EXTENSIONS = ('.csv', '.tsv', '.txt', '.psv', '.tab', '.xlsx', '.xls', '.pdf')


def detect_encoding(path: str | Path) -> str:
    sample_path = Path(path)
    for encoding in ('utf-8-sig', 'utf-8', 'latin-1', 'cp1252'):
        try:
            with sample_path.open('r', encoding=encoding) as handle:
                handle.read(2048)
            return encoding
        except (UnicodeDecodeError, LookupError):
            continue
    return 'utf-8-sig'


def detect_delimiter(path: str | Path) -> str:
    sample_path = Path(path)
    suffix = sample_path.suffix.lower()
    if suffix in {'.tsv', '.tab'}:
        return '\t'
    if suffix == '.psv':
        return '|'

    encoding = detect_encoding(sample_path)
    try:
        with sample_path.open('r', newline='', encoding=encoding) as handle:
            sample = handle.read(4096)
    except Exception:
        return ';'

    if not sample:
        return ';'

    candidates = [';', ',', '\t', '|', ':']
    counts = {candidate: sample.count(candidate) for candidate in candidates}
    # Semicolon preference for European standard if counts tie or are close
    best = max(candidates, key=lambda candidate: counts[candidate])
    return best if counts[best] > 0 else ';'


def _parse_delimited(path: Path) -> tuple[list[str], list[list[str]]]:
    delimiter = detect_delimiter(path)
    encoding = detect_encoding(path)
    with path.open('r', newline='', encoding=encoding) as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        rows = list(reader)

    if not rows:
        return [], []

    # Clean byte order marks or whitespace from headers
    header = [col.replace('\ufeff', '').strip() for col in rows[0]]
    clean_rows = []
    for row in rows[1:]:
        if any(cell.strip() for cell in row):
            clean_rows.append([cell.strip() for cell in row])

    return header, clean_rows


def _parse_excel(path: Path) -> dict[str, tuple[list[str], list[list[str]]]]:
    tables: dict[str, tuple[list[str], list[list[str]]]] = {}
    try:
        import openpyxl  # type: ignore
        wb = openpyxl.load_workbook(path, data_only=True)
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            raw_rows = list(ws.iter_rows(values_only=True))
            if not raw_rows:
                continue

            # Find header row (first row with at least 2 non-empty values)
            header_idx = -1
            for idx, r in enumerate(raw_rows):
                non_empty = [c for c in r if c is not None and str(c).strip()]
                if len(non_empty) >= 2:
                    header_idx = idx
                    break

            if header_idx == -1:
                continue

            header = [str(c).strip() if c is not None else f'Col_{i+1}' for i, c in enumerate(raw_rows[header_idx])]
            
            clean_rows: list[list[str]] = []
            for r in raw_rows[header_idx + 1:]:
                if not any(c is not None and str(c).strip() for c in r):
                    continue
                row_vals: list[str] = []
                for val in r[:len(header)]:
                    if val is None:
                        row_vals.append('')
                    elif isinstance(val, (datetime.date, datetime.datetime)):
                        row_vals.append(val.strftime('%Y-%m-%d'))
                    elif isinstance(val, float) and val.is_integer():
                        row_vals.append(str(int(val)))
                    else:
                        row_vals.append(str(val))
                clean_rows.append(row_vals)

            table_key = f"{path.stem}_{sheet_name}" if len(wb.sheetnames) > 1 else path.stem
            tables[table_key] = (header, clean_rows)
            # Also register sheet_name directly if unambiguous
            if sheet_name not in tables:
                tables[sheet_name] = (header, clean_rows)
        return tables
    except Exception:
        return {}


def _parse_pdf(path: Path) -> dict[str, tuple[list[str], list[list[str]]]]:
    tables: dict[str, tuple[list[str], list[list[str]]]] = {}
    try:
        import pdfplumber  # type: ignore
        with pdfplumber.open(path) as pdf:
            for page_idx, page in enumerate(pdf.pages):
                # Strategy 1: Text layout extraction (ideal for Tufte-style low-ink tables)
                text = page.extract_text() or ''
                lines = [line.strip() for line in text.split('\n') if line.strip()]
                header_idx = -1
                keywords = {'department', 'cost', 'budget', 'actual', 'revenue', 'admissions', 'wbs', 'mrr', 'id', 'date', 'spend', 'variance'}
                for idx, line in enumerate(lines):
                    tokens = [tok.lower().strip(',;') for tok in line.split()]
                    matches = sum(1 for k in keywords if any(k in tok for tok in tokens))
                    if matches >= 2 and len(tokens) >= 3:
                        header_idx = idx
                        break

                if header_idx != -1:
                    header = lines[header_idx].split()
                    rows = []
                    for line in lines[header_idx + 1:]:
                        parts = line.split()
                        if len(parts) >= len(header):
                            n_extra = len(parts) - len(header)
                            col0 = ' '.join(parts[:n_extra + 1])
                            rows.append([col0] + parts[n_extra + 1:])
                    if rows:
                        t_name = path.stem if len(pdf.pages) == 1 else f"{path.stem}_Page{page_idx+1}"
                        tables[t_name] = (header, rows)
                        continue

                # Strategy 2: Grid table extraction fallback
                extracted_tables = page.extract_tables({'vertical_strategy': 'text', 'horizontal_strategy': 'lines'}) or page.extract_tables()
                if extracted_tables:
                    for t_idx, t in enumerate(extracted_tables):
                        if not t or len(t) < 2:
                            continue
                        header = [str(c or '').strip() for c in t[0]]
                        if not any(header):
                            continue
                        rows = [[str(c or '').strip() for c in r] for r in t[1:] if any(c for c in r)]
                        t_name = f"{path.stem}_Page{page_idx+1}_T{t_idx+1}"
                        tables[t_name] = (header, rows)
        return tables
    except Exception:
        return {}


def extract_tables_from_file(path: str | Path) -> dict[str, tuple[list[str], list[list[str]]]]:
    file_path = Path(path)
    suffix = file_path.suffix.lower()

    if suffix in ('.csv', '.tsv', '.txt', '.psv', '.tab'):
        header, rows = _parse_delimited(file_path)
        return {file_path.stem: (header, rows)}
    elif suffix in ('.xlsx', '.xls'):
        return _parse_excel(file_path)
    elif suffix == '.pdf':
        return _parse_pdf(file_path)
    return {}


def extract_all_tables_from_dir(data_dir: str | Path) -> dict[str, tuple[list[str], list[list[str]]]]:
    root = Path(data_dir)
    all_tables: dict[str, tuple[list[str], list[list[str]]]] = {}

    for file_path in sorted(root.iterdir()):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            file_tables = extract_tables_from_file(file_path)
            for t_name, (header, rows) in file_tables.items():
                all_tables[t_name] = (header, rows)
                # Keep exact filename key for direct legacy lookups
                if file_path.suffix.lower() == '.csv' and file_path.name not in all_tables:
                    all_tables[file_path.name] = (header, rows)

    return all_tables


def load_dataset_summary(data_dir: str | Path) -> dict[str, dict[str, Any]]:
    root = Path(data_dir)
    summary: dict[str, dict[str, Any]] = {}

    for file_path in sorted(root.iterdir()):
        if not file_path.is_file():
            continue
        ext = file_path.suffix.lower()
        if ext not in SUPPORTED_EXTENSIONS:
            continue

        file_tables = extract_tables_from_file(file_path)
        if not file_tables:
            # Empty or unreadable file
            summary[file_path.name] = {
                'row_count': 0,
                'column_count': 0,
                'columns': [],
                'source_file': file_path.name,
                'format': ext,
            }
            continue

        for table_name, (header, rows) in file_tables.items():
            key = file_path.name if ext == '.csv' and table_name == file_path.stem else table_name
            summary[key] = {
                'row_count': len(rows),
                'column_count': len(header),
                'columns': header,
                'source_file': file_path.name,
                'format': ext,
            }
            # For backward compatibility with existing tests expecting 'DimDate.csv'
            if ext == '.csv' and file_path.name not in summary:
                summary[file_path.name] = {
                    'row_count': len(rows),
                    'column_count': len(header),
                    'columns': header,
                    'source_file': file_path.name,
                    'format': ext,
                }

    return summary


def stage_dataset_for_sql(data_dir: str | Path, stage_dir: Path | None = None) -> dict[str, Path]:
    root = Path(data_dir)
    target_dir = stage_dir or (root / '.staged_cache')
    target_dir.mkdir(parents=True, exist_ok=True)

    all_tables = extract_all_tables_from_dir(root)
    staged_paths: dict[str, Path] = {}

    for table_name, (header, rows) in all_tables.items():
        if not header:
            continue
        # Sanitize table name for SQL view creation
        safe_name = table_name.replace(' ', '_').replace('-', '_').replace('.', '_')
        csv_file = target_dir / f"{safe_name}.csv"
        with csv_file.open('w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)
        staged_paths[safe_name] = csv_file
        staged_paths[table_name] = csv_file

    return staged_paths
