from pathlib import Path

from multi_agent_analytics.sql_engine import execute_sql


def test_sql_engine_queries_csv():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    results = execute_sql(data_dir, 'SELECT COUNT(*) as cnt FROM DimAccount')
    assert len(results) == 1
    assert int(results[0]['cnt']) > 0


def test_sql_engine_aggregates_kpis():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    results = execute_sql(data_dir, 'SELECT SUM(TRY_CAST(Belop_signert AS DOUBLE)) as total FROM FactGL')
    assert len(results) == 1
    assert results[0]['total'] is not None
