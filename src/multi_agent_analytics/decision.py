from __future__ import annotations

from copy import deepcopy


def generate_prognosis(metrics: dict[str, float]) -> dict[str, dict[str, float | str]]:
    actual_total = float(metrics.get('actual_total', 0.0))
    budget_total = float(metrics.get('budget_total', 0.0))
    forecast_total = float(metrics.get('forecast_total', 0.0))

    baseline = {
        'actual_total': actual_total,
        'expected_total': forecast_total,
        'variance_vs_budget': actual_total - budget_total,
        'scenario': 'baseline',
    }

    conservative = {
        'actual_total': actual_total,
        'expected_total': max(0.0, forecast_total * 0.92),
        'variance_vs_budget': actual_total - budget_total * 0.95,
        'scenario': 'conservative',
    }

    optimistic = {
        'actual_total': actual_total,
        'expected_total': forecast_total * 1.08,
        'variance_vs_budget': actual_total - budget_total * 1.02,
        'scenario': 'optimistic',
    }

    return {
        'baseline': baseline,
        'conservative': conservative,
        'optimistic': optimistic,
    }


def generate_prescriptions(metrics: dict[str, float]) -> list[dict[str, str | float]]:
    actual_total = float(metrics.get('actual_total', 0.0))
    budget_total = float(metrics.get('budget_total', 0.0))
    variance = actual_total - budget_total

    actions = []

    if variance < 0:
        actions.append({
            'title': 'Reduce cost leakage',
            'description': 'Tighten discretionary spending and focus on the highest-impact budget lines.',
            'expected_result': 'Reduce gap to budget by 10-20% within the next cycle.',
            'impact_score': 0.82,
        })

    actions.append({
        'title': 'Prioritize revenue and forecast recovery',
        'description': 'Target the biggest forecast gaps and focus resource allocation on growth levers.',
        'expected_result': 'Lift actual results toward forecast by improving conversion and throughput.',
        'impact_score': 0.76,
    })

    actions.append({
        'title': 'Create scenario-based contingency plan',
        'description': 'Run a conservative, neutral, and optimistic plan above the current baseline.',
        'expected_result': 'Improve decision resilience and reduce downside risk in the next planning cycle.',
        'impact_score': 0.68,
    })

    return actions
