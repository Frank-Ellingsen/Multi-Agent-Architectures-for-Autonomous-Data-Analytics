from pathlib import Path


def test_reporting_skill_pack_has_standard_skill_layout():
    root = Path(__file__).resolve().parents[1] / 'skills' / 'project-finance-ai-reporting-expert-skill'

    assert root.exists()
    assert (root / 'SKILL.md').exists()
    assert (root / 'README.md').exists()
    assert (root / 'references' / 'visual-selection.md').exists()
    assert (root / 'references' / 'html-report-contract.md').exists()
    assert (root / 'references' / 'report-validation.md').exists()
