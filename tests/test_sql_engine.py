from pathlib import Path

from multi_agent_analytics.sql_engine import execute_sql


def test_sql_engine_queries_csv():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    # Find any available table in test_data
    csv_files = [f.stem for f in data_dir.glob('*.csv')]
    assert csv_files, "No CSV files found in test_data"
    target_table = csv_files[0]

    results = execute_sql(data_dir, f'SELECT COUNT(*) as cnt FROM "{target_table}"')
    assert len(results) == 1
    assert int(results[0]['cnt']) > 0


def test_sql_engine_aggregates_kpis():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    csv_files = [f.stem for f in data_dir.glob('*.csv')]
    assert csv_files, "No CSV files found in test_data"
    target_table = csv_files[0]

    results = execute_sql(data_dir, f'SELECT * FROM "{target_table}" LIMIT 5')
    assert len(results) > 0
    assert isinstance(results[0], dict)
