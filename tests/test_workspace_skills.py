from pathlib import Path


def test_workspace_skills_exist_and_have_frontmatter():
    workspace_agents_dir = Path(__file__).resolve().parents[1] / '.agents' / 'skills'

    expected_skills = [
        'autonomous-data-analytics-workflow',
        'reporting-expert',
        'eda-visuals',
        'predictions-prognosis',
        'recommended-actions',
        'orchestration-reporting',
        'powerbi-dashboard-guide',
        'storytelling-with-data-pbi',
    ]

    assert workspace_agents_dir.exists(), ".agents/skills directory must exist"

    for skill_name in expected_skills:
        skill_dir = workspace_agents_dir / skill_name
        skill_file = skill_dir / 'SKILL.md'

        assert skill_dir.exists(), f"Skill directory {skill_name} missing"
        assert skill_file.exists(), f"Skill file {skill_file} missing"

        content = skill_file.read_text(encoding='utf-8')
        assert content.startswith('---'), f"Skill file {skill_file} must start with YAML frontmatter '---'"
        assert 'name:' in content, f"Skill file {skill_file} must contain 'name:' in frontmatter"
        assert 'description:' in content, f"Skill file {skill_file} must contain 'description:' in frontmatter"


def test_reporting_expert_workspace_references_exist():
    refs_dir = Path(__file__).resolve().parents[1] / '.agents' / 'skills' / 'reporting-expert' / 'references'

    assert refs_dir.exists()
    assert (refs_dir / 'html-report-contract.md').exists()
    assert (refs_dir / 'report-validation.md').exists()
    assert (refs_dir / 'visual-selection.md').exists()
