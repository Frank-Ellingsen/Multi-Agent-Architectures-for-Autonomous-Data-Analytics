import pytest

from api import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['skills_count'] == 30


def test_skills_endpoint(client):
    response = client.get('/api/skills')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['skills']) == 30
    assert data['skills'][0]['id'] == '01_inspect_source'


def test_demo_data_endpoint(client):
    response = client.post('/api/demo-data')
    assert response.status_code == 200
    data = response.get_json()
    assert 'metrics' in data
    assert 'prognosis' in data
    assert 'prescriptions' in data
    assert data['metrics']['actual_total'] != 0.0


def test_api_test_key_endpoint_missing_key(client):
    response = client.post('/api/ai/test-key', json={'provider': 'gemini', 'api_key': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] is False
