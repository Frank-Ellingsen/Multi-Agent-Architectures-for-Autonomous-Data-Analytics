from pathlib import Path

from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis


def test_generate_prognosis_returns_scenarios():
    metrics = {
        'actual_total': 1000.0,
        'budget_total': 1200.0,
        'forecast_total': 1100.0,
        'variance_to_budget': -200.0,
        'variance_to_forecast': -100.0,
    }
    prognosis = generate_prognosis(metrics)

    assert set(prognosis.keys()) == {'baseline', 'conservative', 'optimistic'}
    assert prognosis['baseline']['actual_total'] == 1000.0
    assert prognosis['conservative']['expected_total'] < prognosis['baseline']['expected_total']


def test_generate_prescriptions_returns_recommendations():
    metrics = {
        'actual_total': 1000.0,
        'budget_total': 1200.0,
        'forecast_total': 1100.0,
        'variance_to_budget': -200.0,
        'variance_to_forecast': -100.0,
    }
    prescriptions = generate_prescriptions(metrics)

    assert len(prescriptions) >= 2
    assert any(item['title'] for item in prescriptions)
    assert any(item['expected_result'] for item in prescriptions)
