from __future__ import annotations

import csv
from pathlib import Path

from .dataset import detect_delimiter


def _parse_number(value: str | None) -> float:
    if value is None:
        return 0.0
    text = str(value).strip()
    if not text or text.lower() in {'null', 'none', 'n/a', 'na'}:
        return 0.0
    text = text.replace(' ', '')
    try:
        return float(text.replace('.', '').replace(',', '.'))
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return 0.0


def _sum_column(csv_path: str | Path, column: str) -> float:
    path = Path(csv_path)
    with path.open('r', newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle, delimiter=detect_delimiter(path))
        if reader.fieldnames is None or column not in reader.fieldnames:
            return 0.0
        total = 0.0
        for row in reader:
            total += _parse_number(row.get(column))
        return total


def compute_key_metrics(data_dir: str | Path) -> dict[str, float]:
    root = Path(data_dir)
    actual_total = _sum_column(root / 'FactGL.csv', 'Belop_signert')
    budget_total = _sum_column(root / 'FactBudget.csv', 'BudsjettBelop')
    forecast_total = _sum_column(root / 'FactForecast.csv', 'ForecastBelop')
    fte_total = _sum_column(root / 'FactFTE.csv', 'Aarsverk')

    return {
        'actual_total': actual_total,
        'budget_total': budget_total,
        'forecast_total': forecast_total,
        'fte_total': fte_total,
        'variance_to_budget': actual_total - budget_total,
        'variance_to_forecast': actual_total - forecast_total,
    }


def compute_forecast_snapshot(data_dir: str | Path) -> dict[str, float]:
    metrics = compute_key_metrics(data_dir)
    if metrics['budget_total'] == 0:
        budget_pct = 0.0
    else:
        budget_pct = (metrics['actual_total'] / metrics['budget_total']) * 100.0

    if metrics['forecast_total'] == 0:
        forecast_pct = 0.0
    else:
        forecast_pct = (metrics['actual_total'] / metrics['forecast_total']) * 100.0

    return {
        'actual_vs_budget_pct': budget_pct,
        'actual_vs_forecast_pct': forecast_pct,
        'forecast_gap': metrics['forecast_total'] - metrics['actual_total'],
    }
