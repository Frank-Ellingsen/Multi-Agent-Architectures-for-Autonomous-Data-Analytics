"""Benchmark evaluation script running multi-agent analytics across unseen business datasets.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'src'))

from multi_agent_analytics.analytics import compute_forecast_snapshot, compute_key_metrics
from multi_agent_analytics.dataset import extract_all_tables_from_dir, load_dataset_summary
from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis
from multi_agent_analytics.relationships import validate_relationships
from multi_agent_analytics.reporting import build_markdown_report


def evaluate_unseen_portfolio():
    unseen_dir = ROOT / 'test_data' / 'unseen_businesses'
    print("=" * 85)
    print("MULTI-AGENT ARCHITECTURES: BENCHMARK ON UNSEEN MULTI-BUSINESS DATASETS")
    print(f"Landing Zone: {unseen_dir}")
    print("=" * 85)

    summary = load_dataset_summary(unseen_dir)
    print(f"\n--- 1. MULTI-FORMAT INGESTION FOOTPRINT (Skills 01-04) ---")
    print(f"{'Table / Entity Name':<35} {'Format':<10} {'Rows':>8} {'Cols':>6} {'Source File':<30}")
    print("-" * 95)
    for name, info in sorted(summary.items()):
        if name.endswith('.csv') and any(k == name[:-4] for k in summary):
            continue
        fmt = info.get('format', 'unknown').upper().replace('.', '')
        src = info.get('source_file', name)
        print(f"{name:<35} {fmt:<10} {info['row_count']:>8,} {info['column_count']:>6} {src:<30}")

    print(f"\n--- 2. AUTONOMOUS RELATIONSHIP DISCOVERY (Skill 06) ---")
    rel_res = validate_relationships(unseen_dir)
    print(f"Total Discovered/Validated Entity Relationships: {rel_res['relationship_count']}")
    print(f"Referential Integrity Valid:                     {rel_res['valid']}")
    for rel in rel_res.get('relationships', [])[:6]:
        inferred = " [Auto-Inferred]" if rel.get('inferred') else ""
        print(f"  * {rel['FraTabell']}.{rel['FraKolonne']} -> {rel['TilTabell']}.{rel['TilKolonne']}{inferred}")

    print(f"\n--- 3. ADAPTIVE BUSINESS DOMAIN CONTROLLING KPIS (Skill 11) ---")
    metrics = compute_key_metrics(unseen_dir)
    snapshot = compute_forecast_snapshot(unseen_dir)
    currency = metrics.get('currency', 'NOK')
    print(f"Detected Domain:          {metrics.get('domain')}")
    print(f"Monetary Currency:        {currency}")
    print(f"Actual / Primary Total:   {metrics['actual_total']:>15,.2f} {currency}")
    print(f"Budget / Baseline Total:  {metrics['budget_total']:>15,.2f} {currency}")
    print(f"Forecast / EAC Total:     {metrics['forecast_total']:>15,.2f} {currency}")
    print(f"Variance to Budget:       {metrics['variance_to_budget']:>15,.2f} {currency}")
    print(f"Variance to Forecast:     {metrics['variance_to_forecast']:>15,.2f} {currency}")
    print(f"Labor / Capacity Run-Rate:{metrics['fte_total']:>15,.2f}")
    print(f"Actual vs Budget Burn %:  {snapshot['actual_vs_budget_pct']:>14.2f}%")
    print(f"Actual vs Forecast Burn %:{snapshot['actual_vs_forecast_pct']:>14.2f}%")

    print(f"\n--- 4. CONTEXT-AWARE PROGNOSTIC SCENARIOS (Skill 20) ---")
    prognosis = generate_prognosis(metrics)
    for sc_name, sc_data in prognosis.items():
        print(f"  [{sc_name.upper():<12}] Expected: {sc_data['expected_total']:>14,.2f} {currency} | Delta vs Budget: {sc_data['variance_vs_budget']:>14,.2f}")

    print(f"\n--- 5. PRIORITIZED PRESCRIPTIVE ACTIONS (Skill 24) ---")
    prescriptions = generate_prescriptions(metrics)
    for idx, action in enumerate(prescriptions, 1):
        print(f"  {idx}. [Score: {int(action['impact_score']*100)}%] {action['title']}")
        print(f"     Impact: {action['expected_result']}")

    print("\n" + "=" * 85)
    print("Multi-Agent Autonomous Processing of Unseen Multi-Format Data Complete.")
    print("=" * 85)


if __name__ == '__main__':
    evaluate_unseen_portfolio()
