from pathlib import Path

from multi_agent_analytics.analytics import compute_key_metrics
from multi_agent_analytics.relationships import validate_relationships
from multi_agent_analytics.schema import infer_table_schema


def test_schema_inference_reads_semicolon_csv_files():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    schema = infer_table_schema(data_dir)

    assert len(schema) > 0
    # Match any CSV table in test_data
    first_table_name = next(iter(schema.keys()))
    first_table_cols = schema[first_table_name]
    assert len(first_table_cols) > 0
    # Ensure inferred column types are valid schema strings
    assert all(isinstance(t, str) for t in first_table_cols.values())


def test_relationship_validation_passes_for_dataset():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    result = validate_relationships(data_dir)

    assert result['valid'] is True
    assert result['relationship_count'] > 0


def test_key_metrics_are_calculated_from_fact_tables():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    metrics = compute_key_metrics(data_dir)

    assert metrics['actual_total'] != 0.0
    assert metrics['budget_total'] != 0.0
    assert metrics['forecast_total'] != 0.0
    assert metrics['variance_to_budget'] != 0.0
