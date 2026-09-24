# Skill Catalog

This directory contains the modular workflow for autonomous data analytics. Each skill captures a stage in the data-to-decision journey and can be implemented as a prompt, agent task, or workflow component.

## Workflow sequence

1. [01_inspect_source.md](01_inspect_source.md) — inspect the raw source and verify the required data footprint.
2. [02_parse_tabular.md](02_parse_tabular.md) — parse tabular data while preserving structure.
3. [03_parse_excel.md](03_parse_excel.md) — handle spreadsheet inputs and workbook layouts.
4. [04_extract_document.md](04_extract_document.md) — extract values and notes from documents.
5. [05_infer_schema.md](05_infer_schema.md) — infer the expected schema, types, and fields.
6. [06_discover_relationships.md](06_discover_relationships.md) — identify joins and logical connections.
7. [07_profile_quality.md](07_profile_quality.md) — assess completeness, validity, and consistency.
8. [08_normalize_data.md](08_normalize_data.md) — standardize values, units, and categories.
9. [09_build_analytical_model.md](09_build_analytical_model.md) — build the analytical model and metric layer.
10. [10_execute_analytical_sql.md](10_execute_analytical_sql.md) — run transformation logic in SQL.
11. [11_calculate_kpis.md](11_calculate_kpis.md) — compute the key business KPIs.
12. [12_analyze_variance.md](12_analyze_variance.md) — explain deviations from baseline.
13. [13_analyze_trends.md](13_analyze_trends.md) — understand direction and momentum over time.
14. [14_identify_drivers.md](14_identify_drivers.md) — isolate the drivers that change outcomes.
15. [15_detect_anomalies.md](15_detect_anomalies.md) — detect unusual patterns or outliers.
16. [16_apply_status_rag.md](16_apply_status_rag.md) — label outcomes with a status framework.
17. [17_prepare_forecast_dataset.md](17_prepare_forecast_dataset.md) — create data for forecasting.
18. [18_select_and_backtest_model.md](18_select_and_backtest_model.md) — choose and validate a forecasting model.
19. [19_generate_forecast.md](19_generate_forecast.md) — generate the forecast output.
20. [20_generate_scenarios.md](20_generate_scenarios.md) — design strategic scenarios.
21. [21_run_monte_carlo.md](21_run_monte_carlo.md) — quantify uncertainty.
22. [22_run_sensitivity.md](22_run_sensitivity.md) — stress-test assumptions.
23. [23_generate_candidate_actions.md](23_generate_candidate_actions.md) — propose decision options.
24. [24_evaluate_optimize_actions.md](24_evaluate_optimize_actions.md) — score and prioritize actions.
25. [25_calculate_new_balance.md](25_calculate_new_balance.md) — estimate the resulting position after action execution.
26. [26_retrieve_evidence.md](26_retrieve_evidence.md) — gather supporting rationale and traceability.
27. [27_select_build_visuals.md](27_select_build_visuals.md) — choose visuals to communicate the story.
28. [28_build_decision_story.md](28_build_decision_story.md) — turn results into a decision narrative.
29. [29_validate_results.md](29_validate_results.md) — verify outputs before publication.
30. [30_publish_reports.md](30_publish_reports.md) — share the insight package.

## Design principles

- modular task ownership
- traceable evidence and assumptions
- clear data contracts between stages
- reproducible analytic logic
- business-ready reporting outputs
