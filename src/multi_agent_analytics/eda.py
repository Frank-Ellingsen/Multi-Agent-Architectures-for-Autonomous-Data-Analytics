from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

from .dataset import extract_all_tables_from_dir
from .schema import _normalize_numeric, infer_table_schema


def compute_descriptive_stats(data_dir: str | Path) -> dict[str, Any]:
    """Generates column schema profiling and numerical descriptive statistics across all tables."""
    root = Path(data_dir)
    tables = extract_all_tables_from_dir(root)
    table_schemas = infer_table_schema(root)

    column_profiles: list[dict[str, Any]] = []
    numeric_summaries: list[dict[str, Any]] = []

    total_cells = 0
    total_missing = 0

    for table_name, (header, rows) in tables.items():
        if not header:
            continue

        row_count = len(rows)
        types = table_schemas.get(table_name, {})

        for col_idx, col_name in enumerate(header):
            col_type = types.get(col_name, 'string')
            raw_vals = [r[col_idx] for r in rows if col_idx < len(r)]

            non_null_vals = [v for v in raw_vals if v is not None and str(v).strip() and str(v).lower() not in {'null', 'none', 'n/a', 'na'}]
            null_count = row_count - len(non_null_vals)

            total_cells += row_count
            total_missing += null_count

            unique_vals = set(non_null_vals)

            column_profiles.append({
                'table_name': table_name,
                'column_name': col_name,
                'data_type': col_type,
                'total_rows': row_count,
                'non_null_count': len(non_null_vals),
                'null_count': null_count,
                'missing_pct': round((null_count / row_count * 100.0), 1) if row_count > 0 else 0.0,
                'unique_count': len(unique_vals),
            })

            # Numerical statistics if float or integer
            if col_type in ('float', 'integer') and len(non_null_vals) > 0:
                nums = [_normalize_numeric(v) for v in non_null_vals]
                valid_nums = [n for n in nums if n is not None]

                if valid_nums:
                    valid_nums.sort()
                    n = len(valid_nums)
                    total_sum = sum(valid_nums)
                    mean_val = total_sum / n
                    min_val = valid_nums[0]
                    max_val = valid_nums[-1]
                    p25 = valid_nums[int(n * 0.25)]
                    median_val = valid_nums[int(n * 0.50)]
                    p75 = valid_nums[int(n * 0.75)]

                    variance = sum((x - mean_val) ** 2 for x in valid_nums) / n
                    std_dev = math.sqrt(variance)

                    numeric_summaries.append({
                        'table_name': table_name,
                        'column_name': col_name,
                        'count': n,
                        'mean': round(mean_val, 2),
                        'std': round(std_dev, 2),
                        'min': round(min_val, 2),
                        'p25': round(p25, 2),
                        'median': round(median_val, 2),
                        'p75': round(p75, 2),
                        'max': round(max_val, 2),
                        'sum': round(total_sum, 2),
                    })

    overall_missing_pct = round((total_missing / total_cells * 100.0), 2) if total_cells > 0 else 0.0

    return {
        'column_profiles': column_profiles,
        'numeric_summaries': numeric_summaries,
        'total_cells': total_cells,
        'total_missing': total_missing,
        'overall_missing_pct': overall_missing_pct,
    }


def compute_eda_visuals(data_dir: str | Path) -> dict[str, Any]:
    """Generates structured chart data for Exploratory Data Analysis (EDA) visuals."""
    root = Path(data_dir)
    tables = extract_all_tables_from_dir(root)
    table_schemas = infer_table_schema(root)

    category_breakdown: list[dict[str, Any]] = []
    numeric_histogram: list[dict[str, Any]] = []
    time_series_trend: list[dict[str, Any]] = []

    # 1. Dimensional Category Breakdown
    for table_name, (header, rows) in tables.items():
        if not rows or table_name.endswith('.csv') and any(k == table_name[:-4] for k in tables):
            continue

        types = table_schemas.get(table_name, {})
        string_cols = [c for c in header if types.get(c) == 'string' and not re.search(r'(id|nokkel|key|date|dato)', c, re.I)]
        numeric_cols = [c for c in header if types.get(c) in ('float', 'integer')]

        if string_cols and numeric_cols:
            cat_col = string_cols[0]
            num_col = numeric_cols[0]

            cat_idx = header.index(cat_col)
            num_idx = header.index(num_col)

            totals: dict[str, float] = {}
            for r in rows:
                if cat_idx < len(r) and num_idx < len(r):
                    cat_val = str(r[cat_idx]).strip() or 'Other'
                    val = _normalize_numeric(r[num_idx]) or 0.0
                    totals[cat_val] = totals.get(cat_val, 0.0) + val

            sorted_cats = sorted(totals.items(), key=lambda x: abs(x[1]), reverse=True)[:8]
            category_breakdown = [
                {'category': cat, 'value': round(val, 2), 'table': table_name, 'column': cat_col}
                for cat, val in sorted_cats
            ]
            break

    # 2. Numeric Distribution Binned Histogram
    all_numeric_vals: list[float] = []
    for table_name, (header, rows) in tables.items():
        types = table_schemas.get(table_name, {})
        for idx, col in enumerate(header):
            if types.get(col) in ('float', 'integer'):
                vals = [_normalize_numeric(r[idx]) for r in rows if idx < len(r)]
                valid_vals = [v for v in vals if v is not None and v > 0]
                if valid_vals:
                    all_numeric_vals.extend(valid_vals)
                    break

    if all_numeric_vals:
        min_v = min(all_numeric_vals)
        max_v = max(all_numeric_vals)
        if max_v > min_v:
            step = (max_v - min_v) / 5.0
            bins = [min_v + i * step for i in range(6)]
            counts = [0] * 5
            for v in all_numeric_vals:
                idx = min(int((v - min_v) / step), 4)
                counts[idx] += 1

            for i in range(5):
                label = f"{bins[i]:,.0f} - {bins[i+1]:,.0f}"
                numeric_histogram.append({
                    'bin_range': label,
                    'count': counts[i],
                })

    # 3. Time Series Trend if Date/Month exists
    date_col_found = None
    num_col_found = None
    target_rows = []

    for table_name, (header, rows) in tables.items():
        types = table_schemas.get(table_name, {})
        d_cols = [c for c in header if types.get(c) == 'date' or re.search(r'(date|dato|month|maaned|aar)', c, re.I)]
        n_cols = [c for c in header if types.get(c) in ('float', 'integer')]
        if d_cols and n_cols:
            date_col_found = d_cols[0]
            num_col_found = n_cols[0]
            target_rows = (header, rows)
            break

    if date_col_found and target_rows:
        header, rows = target_rows
        d_idx = header.index(date_col_found)
        n_idx = header.index(num_col_found)

        period_totals: dict[str, float] = {}
        for r in rows:
            if d_idx < len(r) and n_idx < len(r):
                raw_d = str(r[d_idx]).strip()
                # Truncate YYYY-MM
                period = raw_d[:7] if len(raw_d) >= 7 else raw_d
                val = _normalize_numeric(r[n_idx]) or 0.0
                period_totals[period] = period_totals.get(period, 0.0) + val

        sorted_periods = sorted(period_totals.items())[:12]
        time_series_trend = [
            {'period': period, 'value': round(val, 2)}
            for period, val in sorted_periods
        ]

    return {
        'category_breakdown': category_breakdown,
        'numeric_histogram': numeric_histogram,
        'time_series_trend': time_series_trend,
    }
