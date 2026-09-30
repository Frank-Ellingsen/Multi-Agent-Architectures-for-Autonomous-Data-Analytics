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
    # Default general business actions
    if variance < 0:
        actions.append({
            'title': 'Reduce cost leakage & discretionary spend',
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


def generate_prognosis_visuals(metrics: dict[str, Any], prognosis: dict[str, Any] | None = None) -> dict[str, Any]:
    """Generates multi-scenario prognostics chart data (Baseline, Conservative, Optimistic)."""
    prog = prognosis or generate_prognosis(metrics)
    currency = metrics.get('currency', 'NOK')
    actual = float(metrics.get('actual_total', 0.0))
    budget = float(metrics.get('budget_total', 0.0))
    forecast = float(metrics.get('forecast_total', 0.0))

    scenarios_list = [
        {
            'name': 'Conservative Scenario (Downside Risk)',
            'key': 'conservative',
            'value': float(prog.get('conservative', {}).get('expected_total', forecast * 0.92)),
            'variance_vs_budget': float(prog.get('conservative', {}).get('variance_vs_budget', actual - budget * 0.95)),
            'color': '#d9381e',  # Tufte muted red highlight
        },
        {
            'name': 'Baseline Scenario (Current EAC/Prognosis)',
            'key': 'baseline',
            'value': float(prog.get('baseline', {}).get('expected_total', forecast)),
            'variance_vs_budget': float(prog.get('baseline', {}).get('variance_vs_budget', actual - budget)),
            'color': '#d97706',  # Tufte amber
        },
        {
            'name': 'Optimistic Scenario (Upside Target)',
            'key': 'optimistic',
            'value': float(prog.get('optimistic', {}).get('expected_total', forecast * 1.08)),
            'variance_vs_budget': float(prog.get('optimistic', {}).get('variance_vs_budget', actual - budget * 1.02)),
            'color': '#10b981',  # Tufte muted green
        },
    ]

    # Generate 6-period trajectory curve for visualization
    periods = ['P-01', 'P-02', 'P-03', 'P-04 (Current)', 'P-05 (Fcst)', 'P-06 (EAC)']
    base_val = actual / 3.0 if actual > 0 else (forecast / 6.0 if forecast > 0 else 100.0)

    trajectory = []
    for i, p in enumerate(periods):
        ratio = (i + 1) / 6.0
        trajectory.append({
            'period': p,
            'actual': round(base_val * (i + 1), 2) if i <= 3 else None,
            'baseline': round((prog.get('baseline', {}).get('expected_total', forecast) or forecast) * ratio, 2),
            'conservative': round((prog.get('conservative', {}).get('expected_total', forecast * 0.92) or forecast) * ratio, 2),
            'optimistic': round((prog.get('optimistic', {}).get('expected_total', forecast * 1.08) or forecast) * ratio, 2),
        })

    return {
        'currency': currency,
        'scenarios': scenarios_list,
        'trajectory': trajectory,
    }


def generate_action_impact_prognosis(metrics: dict[str, Any], prescriptions: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    """Computes new prognose after taking recommended action interventions into consideration."""
    actions = prescriptions or generate_prescriptions(metrics)
    forecast_total = float(metrics.get('forecast_total', 0.0)) or float(metrics.get('actual_total', 0.0))
    budget_total = float(metrics.get('budget_total', 0.0))
    actual_total = float(metrics.get('actual_total', 0.0))
    currency = metrics.get('currency', 'NOK')

    # Quantify individual action impact based on impact score & total volume
    action_impacts = []
    total_savings = 0.0

    for idx, act in enumerate(actions, 1):
        score = float(act.get('impact_score', 0.75))
        # Estimate 3% to 8% cost reduction/recovery per action scaled by impact score
        impact_pct = round(0.04 * score, 4)
        estimated_impact = round(max(5000.0, forecast_total * impact_pct), 2) if forecast_total > 0 else 10000.0 * idx
        total_savings += estimated_impact
        action_impacts.append({
            'title': act.get('title', f'Action {idx}'),
            'impact_score': score,
            'estimated_savings': estimated_impact,
            'impact_pct': round(impact_pct * 100.0, 2),
            'expected_result': act.get('expected_result', ''),
        })

    baseline_prognosis = forecast_total if forecast_total > 0 else actual_total
    conservative_downside = baseline_prognosis * 1.10  # 10% risk escalation
    post_action_prognosis = max(0.0, baseline_prognosis - total_savings)
    net_improvement_pct = round((total_savings / baseline_prognosis * 100.0), 2) if baseline_prognosis > 0 else 0.0

    variance_before = baseline_prognosis - budget_total if budget_total > 0 else 0.0
    variance_after = post_action_prognosis - budget_total if budget_total > 0 else 0.0

    # Waterfall comparison steps
    waterfall_steps = [
        {'step': '1. Original EAC Baseline', 'value': round(baseline_prognosis, 2), 'type': 'base', 'color': '#d97706'},
        {'step': '2. Unmitigated Downside Risk', 'value': round(conservative_downside, 2), 'type': 'risk', 'color': '#d9381e'},
    ]
    for act in action_impacts:
        waterfall_steps.append({
            'step': f"3. Impact: {act['title'][:30]}...",
            'value': -round(act['estimated_savings'], 2),
            'type': 'action',
            'color': '#10b981',
        })
    waterfall_steps.append({
        'step': '4. Post-Action Adjusted Prognosis',
        'value': round(post_action_prognosis, 2),
        'type': 'final',
        'color': '#2563eb',
    })

    return {
        'currency': currency,
        'baseline_prognosis': round(baseline_prognosis, 2),
        'conservative_downside': round(conservative_downside, 2),
        'post_action_prognosis': round(post_action_prognosis, 2),
        'total_action_savings': round(total_savings, 2),
        'net_improvement_pct': net_improvement_pct,
        'variance_before_action': round(variance_before, 2),
        'variance_after_action': round(variance_after, 2),
        'action_impacts': action_impacts,
        'waterfall_steps': waterfall_steps,
    }

