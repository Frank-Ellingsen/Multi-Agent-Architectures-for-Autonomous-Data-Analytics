---
name: autonomous-data-analytics-workflow
description: >-
  Execute the 30-skill modular 6-phase workflow for end-to-end autonomous data analytics,
  financial controlling, project forecasting, and decision storytelling.
---

# Autonomous Data Analytics Workflow (autonomous-data-analytics-workflow)

## Overview
This skill defines the 30-step modular operational workflow for autonomous data analytics, financial controlling, and project forecasting across 6 execution phases.

```mermaid
flowchart LR
    P1[Phase I: Ingestion & Inspection<br/>Skills 01–04] --> P2[Phase II: Schema & Modeling<br/>Skills 05–10]
    P2 --> P3[Phase III: Diagnostics & Metrics<br/>Skills 11–16]
    P3 --> P4[Phase IV: Prognostics & Simulation<br/>Skills 17–22]
    P4 --> P5[Phase V: Prescriptions & Optimization<br/>Skills 23–26]
    P5 --> P6[Phase VI: Storytelling & Publishing<br/>Skills 27–30]
```

## The 6 Workflow Phases

### Phase I: Ingestion & Source Inspection (Skills 01–04)
1. `01_inspect_source` — Inspect raw accounting/ERP sources, encodings, and footprints.
2. `02_parse_tabular` — Parse delimited text files, handling European numbers and quotes.
3. `03_parse_excel` — Extract structured sheets from workbooks, unmerging headers.
4. `04_extract_document` — Extract qualitative context, board memos, and audit notes from business PDFs.

### Phase II: Schema & Dimensional Modeling (Skills 05–10)
5. `05_infer_schema` — Infer physical data types, nullability, unique keys, and dimensional grains.
6. `06_discover_relationships` — Verify star-schema foreign keys and detect orphan transactions.
7. `07_profile_quality` — Profile data completeness, GL debit/credit balances, and duplicate postings.
8. `08_normalize_data` — Standardize sign conventions, currency denominations (NOK/EUR), and ISO dates.
9. `09_build_analytical_model` — Construct the conformed star-schema analytical model.
10. `10_execute_analytical_sql` — Run vectorized transformations and aggregations in DuckDB/SQLite.

### Phase III: Diagnostics & Performance Metrics (Skills 11–16)
11. `11_calculate_kpis` — Compute financial controlling KPIs (Actual, Budget, Forecast, EAC, ETC, FTE).
12. `12_analyze_variance` — Decompose financial variance into Rate, Volume, and Mix waterfall bridges.
13. `13_analyze_trends` — Analyze momentum, moving averages, annualized run-rates, and seasonality.
14. `14_identify_drivers` — Isolate and rank top 20% root-cause drivers causing 80% budget leakage.
15. `15_detect_anomalies` — Flag statistical outliers (Z > 3), missing recurring accruals, and duplicate invoices.
16. `16_apply_status_rag` — Apply deterministic, governed Red-Amber-Green status thresholds.

### Phase IV: Prognostics & Uncertainty Simulation (Skills 17–22)
17. `17_prepare_forecast_dataset` — Engineer time-series lag variables and calendar features.
18. `18_select_and_backtest_model` — Evaluate forecasting algorithms via historical backtesting (MAPE/RMSE).
19. `19_generate_forecast` — Generate forward point estimates with P10/P90 prediction intervals and full-year EAC.
20. `20_generate_scenarios` — Model strategic macro variants (Baseline, Conservative, Optimistic, Stress Test).
21. `21_run_monte_carlo` — Quantify cost/schedule uncertainty through 5,000+ stochastic iterations (P80 contingency).
22. `22_run_sensitivity` — Perform parameter stress testing and construct Tornado sensitivity diagrams.

### Phase V: Prescriptions & Action Optimization (Skills 23–26)
23. `23_generate_candidate_actions` — Propose concrete operational interventions targeted at key drivers.
24. `24_evaluate_optimize_actions` — Score and optimize action portfolio across ROI impact, speed, and risk.
25. `25_calculate_new_balance` — Reconcile before-and-after pro-forma balance and project revised EAC.
26. `26_retrieve_evidence` — Retrieve transaction vouchers, purchase orders, and citations for audit proof.

### Phase VI: Storytelling, Validation & Publishing (Skills 27–30)
27. `27_select_build_visuals` — Build Tufte data-ink visualizations (no vertical lines, direct labels, muted tones).
28. `28_build_decision_story` — Synthesize narrative with Bottom-Line Up Front (BLUF) and executive flow.
29. `29_validate_results` — Independent mathematical gatekeeper audit blocking unverified releases.
30. `30_publish_reports` — Publish accessible, semantic HTML packages with executive print stylesheets.
