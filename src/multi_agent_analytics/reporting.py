from __future__ import annotations

from pathlib import Path

from .analytics import compute_forecast_snapshot, compute_key_metrics
from .dataset import load_dataset_summary
from .relationships import validate_relationships
from .schema import summarize_schema


def build_markdown_report(data_dir: str | Path) -> str:
    root = Path(data_dir)
    dataset_summary = load_dataset_summary(root)
    schema_summary = summarize_schema(root)
    relationship_summary = validate_relationships(root)
    key_metrics = compute_key_metrics(root)
    forecast_snapshot = compute_forecast_snapshot(root)

    lines = [
        '# Data Analytics Report',
        '',
        '## Dataset overview',
        '',
    ]

    for name, info in dataset_summary.items():
        lines.append(f"- {name}: {info['row_count']} rows, {info['column_count']} columns")

    lines.extend([
        '',
        '## Schema summary',
        '',
    ])
    for name, columns in schema_summary.items():
        type_summary = ', '.join(f'{column}: {kind}' for column, kind in columns.items())
        lines.append(f"- {name}: {type_summary}")

    lines.extend([
        '',
        '## Relationship validation',
        '',
        f"- Relationship count: {relationship_summary['relationship_count']}",
        f"- Valid: {relationship_summary['valid']}",
    ])
    if relationship_summary['issues']:
        for issue in relationship_summary['issues']:
            lines.append(f"- Issue: {issue}")

    lines.extend([
        '',
        '## KPI summary',
        '',
        f"- Actual total: {key_metrics['actual_total']:.2f}",
        f"- Budget total: {key_metrics['budget_total']:.2f}",
        f"- Forecast total: {key_metrics['forecast_total']:.2f}",
        f"- Variance to budget: {key_metrics['variance_to_budget']:.2f}",
        f"- Variance to forecast: {key_metrics['variance_to_forecast']:.2f}",
        f"- FTE total: {key_metrics['fte_total']:.2f}",
        f"- Actual vs budget: {forecast_snapshot['actual_vs_budget_pct']:.2f}%",
        f"- Actual vs forecast: {forecast_snapshot['actual_vs_forecast_pct']:.2f}%",
    ])

    return '\n'.join(lines)
