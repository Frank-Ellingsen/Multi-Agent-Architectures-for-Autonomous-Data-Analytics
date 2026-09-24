# Skill Catalog: Autonomous Data-to-Decision Architecture

This catalog defines the modular 30-skill workflow for autonomous data analytics, financial controlling, and project forecasting. Each skill captures a discrete operational responsibility designed for autonomous intelligence agents, controllers, or BI systems.

---

## The 6 Workflow Phases

```mermaid
flowchart LR
    P1[Phase I: Ingestion & Inspection<br/>Skills 01–04] --> P2[Phase II: Schema & Modeling<br/>Skills 05–10]
    P2 --> P3[Phase III: Diagnostics & Metrics<br/>Skills 11–16]
    P3 --> P4[Phase IV: Prognostics & Simulation<br/>Skills 17–22]
    P4 --> P5[Phase V: Prescriptions & Optimization<br/>Skills 23–26]
    P5 --> P6[Phase VI: Storytelling & Publishing<br/>Skills 27–30]
```

---

### Phase I: Ingestion & Source Inspection (Skills 01–04)
1. [01_inspect_source.md](01_inspect_source.md) — Inspect raw accounting/ERP sources, encodings, and verify data footprints.
2. [02_parse_tabular.md](02_parse_tabular.md) — Parse delimited text files, handling European numbers and quote escaping.
3. [03_parse_excel.md](03_parse_excel.md) — Extract structured sheets from workbooks, unmerging headers and resolving formulas.
4. [04_extract_document.md](04_extract_document.md) — Extract qualitative context, board memos, and audit notes from business PDFs.

### Phase II: Schema & Dimensional Modeling (Skills 05–10)
5. [05_infer_schema.md](05_infer_schema.md) — Infer physical data types, nullability, unique keys, and dimensional grains.
6. [06_discover_relationships.md](06_discover_relationships.md) — Verify star-schema foreign keys and detect orphan transactions.
7. [07_profile_quality.md](07_profile_quality.md) — Profile data completeness, general ledger debit/credit balances, and duplicate postings.
8. [08_normalize_data.md](08_normalize_data.md) — Standardize sign conventions, currency denominations (NOK/EUR), and ISO dates.
9. [09_build_analytical_model.md](09_build_analytical_model.md) — Construct the conformed star-schema analytical model.
10. [10_execute_analytical_sql.md](10_execute_analytical_sql.md) — Run vectorized transformations and aggregations in DuckDB or SQLite.

### Phase III: Diagnostics & Performance Metrics (Skills 11–16)
11. [11_calculate_kpis.md](11_calculate_kpis.md) — Compute financial controlling KPIs (Actual, Budget, Forecast, EAC, ETC, FTE).
12. [12_analyze_variance.md](12_analyze_variance.md) — Decompose financial variance into Rate, Volume, and Mix waterfall bridges.
13. [13_analyze_trends.md](13_analyze_trends.md) — Analyze momentum, moving averages, annualized run-rates, and seasonality.
14. [14_identify_drivers.md](14_identify_drivers.md) — Isolate and rank the top 20% root-cause drivers causing 80% of budget leakage.
15. [15_detect_anomalies.md](15_detect_anomalies.md) — Flag statistical outliers (Z > 3), missing recurring accruals, and duplicate invoices.
16. [16_apply_status_rag.md](16_apply_status_rag.md) — Apply deterministic, governed Red-Amber-Green status thresholds.

### Phase IV: Prognostics & Uncertainty Simulation (Skills 17–22)
17. [17_prepare_forecast_dataset.md](17_prepare_forecast_dataset.md) — Engineer time-series lag variables and calendar features.
18. [18_select_and_backtest_model.md](18_select_and_backtest_model.md) — Evaluate forecasting algorithms via historical backtesting (MAPE/RMSE).
19. [19_generate_forecast.md](19_generate_forecast.md) — Generate forward point estimates with P10/P90 prediction intervals and full-year EAC.
20. [20_generate_scenarios.md](20_generate_scenarios.md) — Model strategic macro variants (Baseline, Conservative, Optimistic, Stress Test).
21. [21_run_monte_carlo.md](21_run_monte_carlo.md) — Quantify cost/schedule uncertainty through 5,000+ stochastic iterations (P80 contingency).
22. [22_run_sensitivity.md](22_run_sensitivity.md) — Perform parameter stress testing and construct Tornado sensitivity diagrams.

### Phase V: Prescriptions & Action Optimization (Skills 23–26)
23. [23_generate_candidate_actions.md](23_generate_candidate_actions.md) — Propose concrete, operational interventions targeted at key drivers.
24. [24_evaluate_optimize_actions.md](24_evaluate_optimize_actions.md) — Score and optimize the action portfolio across ROI impact, speed, and risk.
25. [25_calculate_new_balance.md](25_calculate_new_balance.md) — Reconcile before-and-after pro-forma balance and project revised EAC.
26. [26_retrieve_evidence.md](26_retrieve_evidence.md) — Retrieve transaction vouchers, purchase orders, and citations for audit proof.

### Phase VI: Storytelling, Validation & Publishing (Skills 27–30)
27. [27_select_build_visuals.md](27_select_build_visuals.md) — Build Tufte data-ink visualizations (no vertical lines, direct labels, muted tones).
28. [28_build_decision_story.md](28_build_decision_story.md) — Synthesize narrative with Bottom-Line Up Front (BLUF) and executive flow.
29. [29_validate_results.md](29_validate_results.md) — Independent mathematical gatekeeper audit blocking unverified releases.
30. [30_publish_reports.md](30_publish_reports.md) — Publish accessible, semantic HTML packages with executive print stylesheets.

---

## Architectural Principles

- **Deterministic Governance:** Never allow an LLM to assign or override mathematical calculations or RAG statuses.
- **Data-Ink Ratio:** Follow Edward Tufte principles — maximize signal, eliminate decorative clutter, right-align numbers.
- **Traceable Evidence:** Every executive assertion is backed by a transaction voucher or verified audit trail.
- **Local-First Analytics:** High-performance in-memory processing with DuckDB and SQLite with zero external cloud dependencies.
