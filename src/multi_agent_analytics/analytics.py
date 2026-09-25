from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any

from .dataset import detect_delimiter, extract_all_tables_from_dir


def _parse_number(value: str | None) -> float:
    if value is None:
        return 0.0
    text = str(value).strip()
    if not text or text.lower() in {'null', 'none', 'n/a', 'na'}:
        return 0.0
    text = text.replace(' ', '').replace('%', '').replace('$', '').replace('kr', '')
    try:
        if '.' in text and ',' in text:
            # e.g. 1.250,50 or 1,250.50
            if text.rfind(',') > text.rfind('.'):
                text = text.replace('.', '').replace(',', '.')
            else:
                text = text.replace(',', '')
        elif ',' in text:
            # European decimal comma: 1250,50
            text = text.replace(',', '.')
        return float(text)
    except ValueError:
        return 0.0


def _sum_column(csv_path: str | Path, column: str) -> float:
    path = Path(csv_path)
    if not path.exists():
        return 0.0
    with path.open('r', newline='', encoding='utf-8-sig') as handle:
        reader = csv.DictReader(handle, delimiter=detect_delimiter(path))
        if reader.fieldnames is None or column not in reader.fieldnames:
            return 0.0
        total = 0.0
        for row in reader:
            total += _parse_number(row.get(column))
        return total


def detect_business_domain(data_dir: str | Path) -> dict[str, str]:
    """Inspects table names and column names to detect business domain and currency."""
    root = Path(data_dir)
    tables = extract_all_tables_from_dir(root)
    all_names = ' '.join(tables.keys()).lower()
    all_cols = ' '.join(
        ' '.join(header) for header, _ in tables.values()
    ).lower()
    combined = re.sub(r'[_.-]', ' ', f"{all_names} {all_cols}").lower()

    domain_rules = [
        ("Healthcare & Hospital Administration", ["hospital", "admission", "admissions", "bed_days", "occupancy", "clinic", "patient", "icu", "surgery", "healthcare", "pediatrics", "radiology", "oncology"]),
        ("Offshore Marine & Energy Drilling", ["offshore", "drilling", "day rate", "downtime", "rig", "subsea", "fuel cost", "operator"]),
        ("Maritime & Defense Project Controlling", ["wbs", "eac", "etc nok", "cpi", "spi", "corvette", "composite", "hull", "naval", "shipyard", "patrol"]),
        ("Cloud SaaS & Subscription Analytics", ["saas", "mrr", "arr", "churn", "cac", "ltv", "subscription", "seats", "tier", "active seats"]),
        ("Nordic Retail & Supply Chain Operations", ["retail", "artikkel", "vare", "lager", "salg", "innkjop", "margin", "inventory", "sku", "butikk", "varenavn"]),
        ("Management Consulting & Advisory", ["engagement", "billing", "realization", "partner", "consulting", "advisory", "target hours"]),
    ]

    best_domain = "Enterprise Financial Controlling"
    max_score = 0
    for domain, keywords in domain_rules:
        score = sum(1 for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', combined))
        if score > max_score:
            max_score = score
            best_domain = domain

    # Detect currency
    currency = "NOK"
    if "usd" in combined or "$" in combined:
        currency = "USD"
    elif "eur" in combined or "€" in combined:
        currency = "EUR"

    return {
        "domain": best_domain,
        "currency": currency,
        "confidence": "high" if max_score >= 3 else ("medium" if max_score > 0 else "default"),
    }


def compute_key_metrics(data_dir: str | Path) -> dict[str, Any]:
    root = Path(data_dir)

    # 1. Check if legacy Norwegian ERP CSVs exist with expected columns
    fact_gl = root / 'FactGL.csv'
    fact_budget = root / 'FactBudget.csv'
    fact_forecast = root / 'FactForecast.csv'
    fact_fte = root / 'FactFTE.csv'

    if fact_gl.exists() and fact_budget.exists() and fact_forecast.exists():
        actual_total = _sum_column(fact_gl, 'Belop_signert')
        budget_total = _sum_column(fact_budget, 'BudsjettBelop')
        forecast_total = _sum_column(fact_forecast, 'ForecastBelop')
        fte_total = _sum_column(fact_fte, 'Aarsverk')

        return {
            'actual_total': actual_total,
            'budget_total': budget_total,
            'forecast_total': forecast_total,
            'fte_total': fte_total,
            'variance_to_budget': actual_total - budget_total,
            'variance_to_forecast': actual_total - forecast_total,
            'domain': 'Enterprise Financial Controlling (ERP)',
            'currency': 'NOK',
        }

    # 2. Dynamic multi-format, multi-domain metric extraction
    tables = extract_all_tables_from_dir(root)
    domain_info = detect_business_domain(root)

    actual_candidates = [
        'actual_cost_nok', 'actual_cost', 'actual_billing_nok', 'actual', 'actuals',
        'mrr_usd', 'arr_usd', 'maanedlig_salg_nok', 'belop_signert', 'belop',
        'maintenance_actual_usd', 'maintenance_actual_nok', 'kostnad', 'spend', 'sales', 'billing'
    ]
    budget_candidates = [
        'budget_nok', 'budget_cost_nok', 'operating_budget_nok', 'budget_fees_nok',
        'budget_mrr_usd', 'budget', 'budsjett_salg_nok', 'budsjettbelop', 'budsjett',
        'maintenance_budget_usd', 'maintenance_budget_nok', 'plan', 'target'
    ]
    forecast_candidates = [
        'eac_nok', 'eac', 'forecast_cost_nok', 'forecast_billing_nok',
        'forecast_mrr_usd', 'forecast', 'prognose_salg_nok', 'forecastbelop', 'prognose',
        'maintenance_forecast_usd', 'maintenance_forecast_nok', 'etc_nok', 'estimate'
    ]
    labor_candidates = [
        'hours_actual', 'incurred_hours', 'staff_fte', 'crew_fte', 'aarsverk',
        'fte', 'timer', 'hours', 'admissions', 'active_seats', 'lagerbeholdning'
    ]

    def _find_sum(candidates: list[str]) -> float:
        for t_name, (header, rows) in tables.items():
            if t_name.endswith('.csv'):
                continue
            lower_header = {col.lower(): idx for idx, col in enumerate(header)}
            for cand in candidates:
                if cand in lower_header:
                    idx = lower_header[cand]
                    col_sum = sum(_parse_number(r[idx]) for r in rows if idx < len(r))
                    if col_sum != 0.0:
                        return col_sum
        return 0.0

    actual_total = _find_sum(actual_candidates)
    budget_total = _find_sum(budget_candidates)
    forecast_total = _find_sum(forecast_candidates)
    fte_total = _find_sum(labor_candidates)

    # Fallback to any numeric columns if specialized columns not found
    if actual_total == 0.0 and budget_total == 0.0:
        for t_name, (header, rows) in tables.items():
            if t_name.endswith('.csv') or not rows:
                continue
            for idx, col in enumerate(header):
                vals = [_parse_number(r[idx]) for r in rows if idx < len(r)]
                total_val = sum(vals)
                if total_val > 0.0:
                    if actual_total == 0.0:
                        actual_total = total_val
                    elif budget_total == 0.0:
                        budget_total = total_val
                    elif forecast_total == 0.0:
                        forecast_total = total_val

    return {
        'actual_total': actual_total,
        'budget_total': budget_total,
        'forecast_total': forecast_total,
        'fte_total': fte_total,
        'variance_to_budget': actual_total - budget_total,
        'variance_to_forecast': actual_total - forecast_total,
        'domain': domain_info['domain'],
        'currency': domain_info['currency'],
    }


def compute_forecast_snapshot(data_dir: str | Path) -> dict[str, float]:
    metrics = compute_key_metrics(data_dir)
    actual = metrics['actual_total']
    budget = metrics['budget_total']
    forecast = metrics['forecast_total']

    budget_pct = (actual / budget * 100.0) if budget != 0 else 0.0
    forecast_pct = (actual / forecast * 100.0) if forecast != 0 else 0.0

    return {
        'actual_vs_budget_pct': budget_pct,
        'actual_vs_forecast_pct': forecast_pct,
        'forecast_gap': forecast - actual,
    }
