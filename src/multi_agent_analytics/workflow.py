from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Iterable, Sequence


@dataclass(frozen=True)
class Skill:
    id: str
    title: str
    description: str


DEFAULT_SKILLS: tuple[Skill, ...] = (
    Skill("01_inspect_source", "Inspect Source", "Assess raw data sources and constraints."),
    Skill("02_parse_tabular", "Parse Tabular", "Normalize tabular inputs into a clean table structure."),
    Skill("03_parse_excel", "Parse Excel", "Read workbook tabs and ranges into a consistent analytical format."),
    Skill("04_extract_document", "Extract Document", "Pull facts from documents, PDFs, and unstructured notes."),
    Skill("05_infer_schema", "Infer Schema", "Infer field types, keys, and logical structure."),
    Skill("06_discover_relationships", "Discover Relationships", "Identify connections between entities and datasets."),
    Skill("07_profile_quality", "Profile Quality", "Assess completeness, duplication, and validity."),
    Skill("08_normalize_data", "Normalize Data", "Standardize naming, units, categories, and values."),
    Skill("09_build_analytical_model", "Build Analytical Model", "Define the analytical model and dimensions."),
    Skill("10_execute_analytical_sql", "Execute Analytical SQL", "Build the analytical table layer in SQL."),
    Skill("11_calculate_kpis", "Calculate KPIs", "Compute business performance indicators."),
    Skill("12_analyze_variance", "Analyze Variance", "Explain deltas against baselines and forecasts."),
    Skill("13_analyze_trends", "Analyze Trends", "Identify trend and time-based signals."),
    Skill("14_identify_drivers", "Identify Drivers", "Isolate the variables affecting outcomes."),
    Skill("15_detect_anomalies", "Detect Anomalies", "Flag outliers and abnormal behavior."),
    Skill("16_apply_status_rag", "Apply Status RAG", "Classify business outcomes using red, amber, green status."),
    Skill("17_prepare_forecast_dataset", "Prepare Forecast Dataset", "Prepare time-series features for forecasting."),
    Skill("18_select_and_backtest_model", "Select and Backtest Model", "Choose the best model and validate it historically."),
    Skill("19_generate_forecast", "Generate Forecast", "Create expected future values and confidence signals."),
    Skill("20_generate_scenarios", "Generate Scenarios", "Build strategic scenario variants."),
    Skill("21_run_monte_carlo", "Run Monte Carlo", "Quantify risk and uncertainty through simulation."),
    Skill("22_run_sensitivity", "Run Sensitivity", "Stress-test assumptions and key drivers."),
    Skill("23_generate_candidate_actions", "Generate Candidate Actions", "Produce action options tied to the findings."),
    Skill("24_evaluate_optimize_actions", "Evaluate and Optimize Actions", "Score the actions by impact, risk, and viability."),
    Skill("25_calculate_new_balance", "Calculate New Balance", "Project the target state after action execution."),
    Skill("26_retrieve_evidence", "Retrieve Evidence", "Capture the supporting evidence for decisions."),
    Skill("27_select_build_visuals", "Select and Build Visuals", "Choose visuals for communicating the story."),
    Skill("28_build_decision_story", "Build Decision Story", "Turn business analysis into a decision narrative."),
    Skill("29_validate_results", "Validate Results", "Check correctness and business alignment."),
    Skill("30_publish_reports", "Publish Reports", "Prepare and distribute the final report."),
)

SKILL_INDEX = {skill.id: skill for skill in DEFAULT_SKILLS}


def build_workflow(start: int = 1, end: int | None = None) -> list[Skill]:
    if end is None:
        end = len(DEFAULT_SKILLS)

    if start < 1 or end < start:
        raise ValueError("start must be >= 1 and end must be >= start")
    if end > len(DEFAULT_SKILLS):
        raise ValueError(f"end must be <= {len(DEFAULT_SKILLS)}")

    return list(DEFAULT_SKILLS[start - 1 : end])


def get_skill_summary() -> list[str]:
    return [skill.title for skill in DEFAULT_SKILLS]


def run_workflow(skill_ids: Sequence[str], handler: Callable[[Skill], Any]) -> list[Any]:
    missing = [skill_id for skill_id in skill_ids if skill_id not in SKILL_INDEX]
    if missing:
        raise ValueError(f"Unknown skill id(s): {missing}")

    return [handler(SKILL_INDEX[skill_id]) for skill_id in skill_ids]
