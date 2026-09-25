from __future__ import annotations

from typing import Any


def generate_prognosis(metrics: dict[str, Any]) -> dict[str, dict[str, float | str]]:
    actual_total = float(metrics.get('actual_total', 0.0))
    budget_total = float(metrics.get('budget_total', 0.0))
    forecast_total = float(metrics.get('forecast_total', 0.0))
    domain = str(metrics.get('domain', 'Enterprise Financial Controlling'))

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


def generate_prescriptions(metrics: dict[str, Any]) -> list[dict[str, str | float]]:
    actual_total = float(metrics.get('actual_total', 0.0))
    budget_total = float(metrics.get('budget_total', 0.0))
    variance = actual_total - budget_total
    domain = str(metrics.get('domain', '')).lower()
    currency = metrics.get('currency', 'NOK')

    actions: list[dict[str, str | float]] = []

    if 'maritime' in domain or 'defense' in domain:
        actions.append({
            'title': 'EAC Baseline Review & WBS Composite Cost Containment',
            'description': 'Audit composite manufacturing hours on WP-100 and enforce fixed-price subcontracting on propulsion milestones.',
            'expected_result': f'Contain cost overrun within contingency reserve ({currency} 15M target savings).',
            'impact_score': 0.92,
        })
        actions.append({
            'title': 'Milestone Critical Path Recovery (Gas Turbine Alignment)',
            'description': 'Allocate dedicated engineering squad to clear mechanical integration bottlenecks prior to Harbor Acceptance Tests (HAT).',
            'expected_result': 'Recover 3 weeks schedule slippage (SPI improvement from 0.94 to 0.99).',
            'impact_score': 0.88,
        })
        actions.append({
            'title': 'Management Reserve Drawdown Governance',
            'description': 'Require formal Project Controller sign-off for WP-900 contingency allocation release.',
            'expected_result': 'Protect remaining risk reserve through sea trials delivery.',
            'impact_score': 0.78,
        })
        return actions

    if 'saas' in domain or 'subscription' in domain:
        actions.append({
            'title': 'High Churn Risk Enterprise Intervention',
            'description': 'Deploy dedicated Customer Success engineers to accounts with churn score > 0.30.',
            'expected_result': 'Preserve MRR run-rate and reduce annual revenue churn by 15-25%.',
            'impact_score': 0.89,
        })
        actions.append({
            'title': 'Annual Prepayment Contract Incentive',
            'description': 'Offer 10% discount on 2-year upfront commitment to convert monthly cash flow.',
            'expected_result': 'Improve Net Revenue Retention (NRR) and reduce CAC payback period.',
            'impact_score': 0.81,
        })
        return actions

    if 'retail' in domain or 'supply chain' in domain:
        actions.append({
            'title': 'Slow-Moving Stock Liquidation & Warehouse Rebalancing',
            'description': 'Reallocate high-inventory outerwear from regional hubs to high-turnover metropolitan stores.',
            'expected_result': 'Free up working capital and reduce inventory holding cost by 12%.',
            'impact_score': 0.84,
        })
        actions.append({
            'title': 'Margin Defense on Premium Product Lines',
            'description': 'Enforce minimum price thresholds on high-margin categories (58%+ gross margin).',
            'expected_result': 'Lift net realized gross profit by 2.4 percentage points.',
            'impact_score': 0.79,
        })
        return actions

    if 'hospital' in domain or 'healthcare' in domain:
        actions.append({
            'title': 'Emergency & ICU Clinical Overtime Rationalization',
            'description': 'Review nurse shift scheduling and align nursing staff rosters with peak intake periods.',
            'expected_result': f'Reduce unscheduled overtime premium spend by {currency} 4.2M.',
            'impact_score': 0.87,
        })
        actions.append({
            'title': 'Bed Occupancy & Post-Op Discharge Protocol',
            'description': 'Standardize early morning discharge clearances to maintain target 85-90% bed occupancy.',
            'expected_result': 'Eliminate elective surgery postponement caused by ICU bed lock.',
            'impact_score': 0.82,
        })
        return actions

    # Default general business actions
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
