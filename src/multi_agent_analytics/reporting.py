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

    domain = key_metrics.get('domain', 'Enterprise Financial Controlling')
    currency = key_metrics.get('currency', 'NOK')

    lines = [
        '# Executive Data Analytics Report',
        '',
        f"**Business Domain:** {domain}  ",
        f"**Monetary Currency:** {currency}  ",
        '',
        '## Dataset Footprint & Format Overview',
        '',
    ]

    for name, info in dataset_summary.items():
        if name.endswith('.csv') and any(k == name[:-4] for k in dataset_summary):
            continue
        fmt = info.get('format', 'tabular').upper().replace('.', '')
        src = info.get('source_file', name)
        lines.append(f"- **{name}** ({fmt}): {info['row_count']} rows, {info['column_count']} columns (Source: `{src}`)")

    lines.extend([
        '',
        '## Schema Inference & Dimensional Architecture',
        '',
    ])
    for name, columns in schema_summary.items():
        if name.endswith('.csv') and any(k == name[:-4] for k in schema_summary):
            continue
        type_summary = ', '.join(f'{column}: {kind}' for column, kind in list(columns.items())[:8])
        if len(columns) > 8:
            type_summary += f", ... (+{len(columns)-8} more)"
        lines.append(f"- **{name}**: {type_summary}")

    lines.extend([
        '',
        '## Relationship Discovery & Dimensional Integrity',
        '',
        f"- Discovered/Validated Relationships: {relationship_summary['relationship_count']}",
        f"- Referential Integrity Valid: {relationship_summary['valid']}",
    ])
    if relationship_summary.get('relationships'):
        for rel in relationship_summary['relationships'][:5]:
            inferred = " (auto-inferred)" if rel.get('inferred') else ""
            lines.append(f"  - `{rel['FraTabell']}.{rel['FraKolonne']}` -> `{rel['TilTabell']}.{rel['TilKolonne']}`{inferred}")
    if relationship_summary['issues']:
        for issue in relationship_summary['issues']:
            lines.append(f"- Issue: {issue}")

    lines.extend([
        '',
        '## Deterministic KPI Audit (Tufte Data-Ink)',
        '',
        f"- Actual total: {key_metrics['actual_total']:,.2f} {currency}",
        f"- Budget total: {key_metrics['budget_total']:,.2f} {currency}",
        f"- Forecast total: {key_metrics['forecast_total']:,.2f} {currency}",
        f"- Variance to budget: {key_metrics['variance_to_budget']:,.2f} {currency}",
        f"- Variance to forecast: {key_metrics['variance_to_forecast']:,.2f} {currency}",
        f"- FTE / Labor volume run rate: {key_metrics['fte_total']:,.2f}",
        f"- Actual vs budget: {forecast_snapshot['actual_vs_budget_pct']:.2f}%",
        f"- Actual vs forecast: {forecast_snapshot['actual_vs_forecast_pct']:.2f}%",
    ])

    return '\n'.join(lines)
