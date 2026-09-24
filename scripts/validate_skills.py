from pathlib import Path

EXPECTED_SKILLS = [
    '01_inspect_source.md',
    '02_parse_tabular.md',
    '03_parse_excel.md',
    '04_extract_document.md',
    '05_infer_schema.md',
    '06_discover_relationships.md',
    '07_profile_quality.md',
    '08_normalize_data.md',
    '09_build_analytical_model.md',
    '10_execute_analytical_sql.md',
    '11_calculate_kpis.md',
    '12_analyze_variance.md',
    '13_analyze_trends.md',
    '14_identify_drivers.md',
    '15_detect_anomalies.md',
    '16_apply_status_rag.md',
    '17_prepare_forecast_dataset.md',
    '18_select_and_backtest_model.md',
    '19_generate_forecast.md',
    '20_generate_scenarios.md',
    '21_run_monte_carlo.md',
    '22_run_sensitivity.md',
    '23_generate_candidate_actions.md',
    '24_evaluate_optimize_actions.md',
    '25_calculate_new_balance.md',
    '26_retrieve_evidence.md',
    '27_select_build_visuals.md',
    '28_build_decision_story.md',
    '29_validate_results.md',
    '30_publish_reports.md',
]

root = Path(__file__).resolve().parent.parent
skill_dir = root / 'skills'
missing = [name for name in EXPECTED_SKILLS if not (skill_dir / name).exists()]

if missing:
    raise SystemExit(f'Missing expected skill files: {missing}')

print(f'Validated {len(EXPECTED_SKILLS)} skill files in {skill_dir}.')
