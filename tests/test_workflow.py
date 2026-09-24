from pathlib import Path

from multi_agent_analytics.dataset import load_dataset_summary
from multi_agent_analytics.workflow import DEFAULT_SKILLS, build_workflow, run_workflow


def test_default_skill_count():
    assert len(DEFAULT_SKILLS) == 30


def test_build_workflow_returns_requested_range():
    workflow = build_workflow(1, 3)
    assert [skill.id for skill in workflow] == [
        '01_inspect_source',
        '02_parse_tabular',
        '03_parse_excel',
    ]


def test_run_workflow_executes_all_skills():
    results = run_workflow(
        ['01_inspect_source', '02_parse_tabular'],
        lambda skill: {"id": skill.id, "title": skill.title},
    )

    assert results == [
        {"id": "01_inspect_source", "title": "Inspect Source"},
        {"id": "02_parse_tabular", "title": "Parse Tabular"},
    ]


def test_dataset_summary_reads_semicolon_data():
    root = Path(__file__).resolve().parents[1] / 'test_data'
    summary = load_dataset_summary(root)

    assert 'DimDate.csv' in summary
    assert summary['DimDate.csv']['row_count'] == 730
    assert summary['DimDate.csv']['column_count'] == 7
