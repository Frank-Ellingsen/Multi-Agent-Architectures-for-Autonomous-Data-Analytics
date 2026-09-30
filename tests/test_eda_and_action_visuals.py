from pathlib import Path

from multi_agent_analytics.analytics import compute_key_metrics
from multi_agent_analytics.decision import (
    generate_action_impact_prognosis,
    generate_prescriptions,
    generate_prognosis,
    generate_prognosis_visuals,
)
from multi_agent_analytics.eda import compute_descriptive_stats, compute_eda_visuals


def test_descriptive_stats_and_eda_visuals_for_default_erp():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    stats = compute_descriptive_stats(data_dir)

    assert stats['total_cells'] > 0
    assert len(stats['column_profiles']) > 0
    assert len(stats['numeric_summaries']) > 0

    eda = compute_eda_visuals(data_dir)
    assert 'category_breakdown' in eda
    assert 'numeric_histogram' in eda
    assert 'time_series_trend' in eda


def test_prognosis_visuals_and_action_impact_simulation():
    data_dir = Path(__file__).resolve().parents[1] / 'test_data'
    metrics = compute_key_metrics(data_dir)
    prognosis = generate_prognosis(metrics)
    prescriptions = generate_prescriptions(metrics)

    prog_vis = generate_prognosis_visuals(metrics, prognosis)
    assert 'scenarios' in prog_vis
    assert len(prog_vis['scenarios']) == 3
    assert 'trajectory' in prog_vis

    action_impact = generate_action_impact_prognosis(metrics, prescriptions)
    assert 'baseline_prognosis' in action_impact
    assert 'post_action_prognosis' in action_impact
    assert 'total_action_savings' in action_impact
    assert 'waterfall_steps' in action_impact
    assert len(action_impact['waterfall_steps']) >= 4


def test_unseen_business_domains_generate_stats_and_visuals():
    unseen_dir = Path(__file__).resolve().parents[1] / 'test_data' / 'unseen_businesses'
    for file_path in unseen_dir.glob('*.*'):
        if file_path.name.startswith('.'):
            continue
        # Check single file folder test
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            import shutil
            shutil.copy2(file_path, tmp_path / file_path.name)
            metrics = compute_key_metrics(tmp_path)
            stats = compute_descriptive_stats(tmp_path)
            eda = compute_eda_visuals(tmp_path)
            prescriptions = generate_prescriptions(metrics)
            impact = generate_action_impact_prognosis(metrics, prescriptions)

            assert metrics['domain'] != ''
            assert stats['total_cells'] >= 0
            assert 'category_breakdown' in eda
            assert impact['post_action_prognosis'] >= 0
