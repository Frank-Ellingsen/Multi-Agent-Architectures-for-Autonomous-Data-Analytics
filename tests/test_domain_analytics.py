from pathlib import Path
import shutil
import tempfile
import pytest

from multi_agent_analytics.analytics import compute_key_metrics, detect_business_domain
from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis
from multi_agent_analytics.relationships import validate_relationships
from multi_agent_analytics.reporting import build_markdown_report

DATA_DIR = Path(__file__).resolve().parents[1] / 'test_data' / 'unseen_businesses'


def _test_single_file_domain(filename: str) -> dict:
    with tempfile.TemporaryDirectory() as temp_dir:
        dest = Path(temp_dir)
        shutil.copy2(DATA_DIR / filename, dest / filename)
        metrics = compute_key_metrics(dest)
        prognosis = generate_prognosis(metrics)
        prescriptions = generate_prescriptions(metrics)
        report = build_markdown_report(dest)
        relationships = validate_relationships(dest)
        return {
            'metrics': metrics,
            'prognosis': prognosis,
            'prescriptions': prescriptions,
            'report': report,
            'relationships': relationships,
        }


def test_maritime_defense_project_controlling_analytics():
    res = _test_single_file_domain('maritime_defense_vessel.xlsx')
    metrics = res['metrics']
    assert 'Maritime & Defense' in metrics['domain']
    assert metrics['currency'] == 'NOK'
    assert metrics['actual_total'] > 100_000_000.0  # Over 100M NOK
    assert metrics['budget_total'] > 100_000_000.0
    assert metrics['forecast_total'] > 100_000_000.0
    assert metrics['fte_total'] > 1000.0  # Over 1000 composite labor hours

    # Prescriptions should mention composite, EAC, or WBS
    prescriptions = res['prescriptions']
    assert len(prescriptions) > 0
    all_text = ' '.join(f"{p['title']} {p['description']}" for p in prescriptions).lower()
    assert 'wbs' in all_text or 'composite' in all_text or 'reserve' in all_text


def test_saas_subscription_analytics():
    res = _test_single_file_domain('saas_subscription_platform.tsv')
    metrics = res['metrics']
    assert 'SaaS' in metrics['domain']
    assert metrics['currency'] == 'USD'
    assert metrics['actual_total'] > 50_000.0  # MRR sum
    assert metrics['budget_total'] > 50_000.0

    prescriptions = res['prescriptions']
    assert len(prescriptions) > 0
    all_text = ' '.join(f"{p['title']} {p['description']}" for p in prescriptions).lower()
    assert 'churn' in all_text or 'mrr' in all_text


def test_nordic_retail_inventory_analytics():
    res = _test_single_file_domain('nordic_retail_inventory.csv')
    metrics = res['metrics']
    assert 'Retail' in metrics['domain']
    assert metrics['actual_total'] > 1_000_000.0  # Monthly sales NOK
    assert metrics['variance_to_budget'] != 0.0

    prescriptions = res['prescriptions']
    all_text = ' '.join(f"{p['title']} {p['description']}" for p in prescriptions).lower()
    assert 'inventory' in all_text or 'margin' in all_text or 'stock' in all_text


def test_offshore_marine_drilling_analytics():
    res = _test_single_file_domain('offshore_marine_drilling.psv')
    metrics = res['metrics']
    assert 'Offshore' in metrics['domain']
    assert metrics['actual_total'] > 1_000_000.0  # Maintenance actual USD
    assert metrics['fte_total'] > 100.0  # Crew FTE total


def test_hospital_kpi_pdf_analytics():
    res = _test_single_file_domain('hospital_executive_kpis.pdf')
    metrics = res['metrics']
    assert 'Healthcare' in metrics['domain']
    assert metrics['actual_total'] > 10_000_000.0  # Hospital actual cost NOK
    assert metrics['budget_total'] > 10_000_000.0

    prescriptions = res['prescriptions']
    all_text = ' '.join(f"{p['title']} {p['description']}" for p in prescriptions).lower()
    assert 'hospital' in all_text or 'icu' in all_text or 'overtime' in all_text or 'bed' in all_text


def test_consulting_engagements_analytics():
    res = _test_single_file_domain('management_consulting_engagements.txt')
    metrics = res['metrics']
    assert 'Consulting' in metrics['domain']
    assert metrics['actual_total'] > 10_000_000.0  # Actual billed fees NOK
    assert metrics['fte_total'] > 5000.0  # Incurred hours
