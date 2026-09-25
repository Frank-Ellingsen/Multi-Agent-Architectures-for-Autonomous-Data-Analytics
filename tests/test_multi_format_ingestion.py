from pathlib import Path
import pytest

from multi_agent_analytics.dataset import (
    SUPPORTED_EXTENSIONS,
    detect_delimiter,
    extract_all_tables_from_dir,
    extract_tables_from_file,
    load_dataset_summary,
    stage_dataset_for_sql,
)
from multi_agent_analytics.schema import infer_table_schema
from multi_agent_analytics.sql_engine import execute_sql

DATA_DIR = Path(__file__).resolve().parents[1] / 'test_data' / 'unseen_businesses'


def test_maritime_defense_excel_ingestion():
    excel_file = DATA_DIR / 'maritime_defense_vessel.xlsx'
    assert excel_file.exists()

    tables = extract_tables_from_file(excel_file)
    assert len(tables) >= 3
    # Check sheets exist
    assert any('WBS_Cost_Control' in name for name in tables)
    assert any('Project_Summary' in name for name in tables)
    assert any('Milestone_Risk' in name for name in tables)

    # Check WBS table content
    wbs_key = next(k for k in tables if 'WBS_Cost_Control' in k)
    header, rows = tables[wbs_key]
    assert 'WBS_Code' in header
    assert 'Budget_NOK' in header
    assert 'Actual_Cost_NOK' in header
    assert 'EAC_NOK' in header
    assert len(rows) == 6


def test_saas_tsv_tab_separator_detection():
    tsv_file = DATA_DIR / 'saas_subscription_platform.tsv'
    assert tsv_file.exists()

    delim = detect_delimiter(tsv_file)
    assert delim == '\t'

    tables = extract_tables_from_file(tsv_file)
    assert 'saas_subscription_platform' in tables
    header, rows = tables['saas_subscription_platform']
    assert 'mrr_usd' in header
    assert 'arr_usd' in header
    assert 'churn_risk_score' in header
    assert len(rows) == 10


def test_nordic_retail_semicolon_csv_detection():
    csv_file = DATA_DIR / 'nordic_retail_inventory.csv'
    assert csv_file.exists()

    delim = detect_delimiter(csv_file)
    assert delim == ';'

    tables = extract_tables_from_file(csv_file)
    assert 'nordic_retail_inventory' in tables
    header, rows = tables['nordic_retail_inventory']
    assert 'Artikkel_ID' in header
    assert 'Innkjoepspris_NOK' in header
    assert 'Bruttomargin_Prosent' in header
    assert len(rows) == 8


def test_offshore_marine_pipe_psv_detection():
    psv_file = DATA_DIR / 'offshore_marine_drilling.psv'
    assert psv_file.exists()

    delim = detect_delimiter(psv_file)
    assert delim == '|'

    tables = extract_tables_from_file(psv_file)
    assert 'offshore_marine_drilling' in tables
    header, rows = tables['offshore_marine_drilling']
    assert 'vessel_name' in header
    assert 'day_rate_usd' in header
    assert 'maintenance_actual_usd' in header
    assert len(rows) == 5


def test_hospital_kpi_pdf_table_extraction():
    pdf_file = DATA_DIR / 'hospital_executive_kpis.pdf'
    assert pdf_file.exists()

    tables = extract_tables_from_file(pdf_file)
    assert len(tables) >= 1
    # Check that hospital department rows were extracted
    first_table = list(tables.values())[0]
    header, rows = first_table
    assert any('department' in col.lower() for col in header)
    assert any('cost' in col.lower() or 'budget' in col.lower() for col in header)
    assert len(rows) >= 5


def test_consulting_txt_comma_detection():
    txt_file = DATA_DIR / 'management_consulting_engagements.txt'
    assert txt_file.exists()

    tables = extract_tables_from_file(txt_file)
    assert 'management_consulting_engagements' in tables
    header, rows = tables['management_consulting_engagements']
    assert 'engagement_id' in header
    assert 'actual_billing_nok' in header
    assert len(rows) == 5


def test_multi_format_dataset_summary():
    summary = load_dataset_summary(DATA_DIR)
    assert len(summary) >= 6

    # Verify formats are labeled
    formats = {info['format'] for info in summary.values()}
    assert '.xlsx' in formats or '.tsv' in formats


def test_sql_engine_queries_excel_and_tsv_via_duckdb():
    results = execute_sql(
        DATA_DIR,
        "SELECT COUNT(*) as row_count FROM saas_subscription_platform"
    )
    assert len(results) == 1
    assert int(results[0]['row_count']) == 10
