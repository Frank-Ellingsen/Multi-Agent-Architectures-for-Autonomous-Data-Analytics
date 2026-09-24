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
