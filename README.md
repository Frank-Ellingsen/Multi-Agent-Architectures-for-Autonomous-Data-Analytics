# Multi-Agent Architectures for Autonomous Data Analytics

A GitHub-ready repository for a multi-agent analytics workflow that converts fragmented business inputs into decision-ready insights. The design is intentionally modular: each skill is a discrete responsibility that an orchestrator, agent team, or human analyst can run in sequence.

## Why this project exists

Most organizations struggle with analytics workflows spread across spreadsheets, PDFs, ERP exports, and operational systems. This project defines a repeatable architecture for intelligence agents to:

- inspect source material
- parse tabular data and spreadsheets
- extract document facts
- infer schema and relationships
- profile quality and normalize values
- build an analytical model
- calculate KPI and trend metrics
- identify drivers, anomalies, and variance
- prepare forecasts and scenarios
- evaluate actions and publish a decision-ready story

## Workflow overview

```text
source data -> inspect -> parse -> normalize -> model -> analyze -> forecast -> optimize -> decide -> publish
```

## Repository structure

```text
.
├── README.md
├── LICENSE
├── .gitignore
├── .github/
│   └── workflows/
│       └── validate-skills.yml
├── docs/
│   └── roadmap.md
├── scripts/
│   └── validate_skills.py
├── skills/
│   ├── README.md
│   ├── 01_inspect_source.md
│   ├── 02_parse_tabular.md
│   ├── 03_parse_excel.md
│   ├── 04_extract_document.md
│   ├── 05_infer_schema.md
│   ├── 06_discover_relationships.md
│   ├── 07_profile_quality.md
│   ├── 08_normalize_data.md
│   ├── 09_build_analytical_model.md
│   ├── 10_execute_analytical_sql.md
│   ├── 11_calculate_kpis.md
│   ├── 12_analyze_variance.md
│   ├── 13_analyze_trends.md
│   ├── 14_identify_drivers.md
│   ├── 15_detect_anomalies.md
│   ├── 16_apply_status_rag.md
│   ├── 17_prepare_forecast_dataset.md
│   ├── 18_select_and_backtest_model.md
│   ├── 19_generate_forecast.md
│   ├── 20_generate_scenarios.md
│   ├── 21_run_monte_carlo.md
│   ├── 22_run_sensitivity.md
│   ├── 23_generate_candidate_actions.md
│   ├── 24_evaluate_optimize_actions.md
│   ├── 25_calculate_new_balance.md
│   ├── 26_retrieve_evidence.md
│   ├── 27_select_build_visuals.md
│   ├── 28_build_decision_story.md
│   ├── 29_validate_results.md
│   └── 30_publish_reports.md
└──
```

## Getting started

1. Review the workflow in [skills/README.md](skills/README.md).
2. Move through the skills in order from source inspection to publishing.
3. Adapt each stage to your own data, system architecture, or agent orchestration platform.

## Recommended use cases

- prompt library for multi-agent analytics systems
- orchestration framework for autonomous business analysis
- template for AI-assisted forecasting and decision support
- playbook for data prep, analysis, and reporting

## Quick start

```bash
python -m multi_agent_analytics --start 1 --end 5
```

This prints the first five stages of the workflow and confirms the runtime can load the skill catalog.

## Validation

A lightweight validation script checks that the expected skill files exist in the repository.

```bash
python scripts/validate_skills.py
python -m pytest -q
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
