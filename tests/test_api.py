import io
from pathlib import Path
import pytest

from api import app

DATA_DIR = Path(__file__).resolve().parents[1] / 'test_data' / 'unseen_businesses'


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
    assert '.xlsx' in data['supported_extensions']
    assert '.pdf' in data['supported_extensions']


def test_skills_endpoint(client):
    response = client.get('/api/skills')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['skills']) == 30
    assert data['skills'][0]['id'] == '01_inspect_source'


def test_demo_domains_endpoint(client):
    response = client.get('/api/demo-domains')
    assert response.status_code == 200
    data = response.get_json()
    assert 'domains' in data
    assert len(data['domains']) >= 6


def test_demo_data_default_erp(client):
    response = client.post('/api/demo-data', json={'domain': 'erp_default'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'metrics' in data
    assert data['metrics']['actual_total'] != 0.0


def test_demo_data_maritime_defense(client):
    response = client.post('/api/demo-data', json={'domain': 'maritime_defense'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'metrics' in data
    assert 'Maritime & Defense' in data['metrics']['domain']
    assert data['metrics']['actual_total'] > 100_000_000.0


def test_demo_data_saas(client):
    response = client.post('/api/demo-data', json={'domain': 'saas_subscription'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'metrics' in data
    assert 'SaaS' in data['metrics']['domain']


def test_demo_data_hospital_pdf(client):
    response = client.post('/api/demo-data', json={'domain': 'hospital_kpis'})
    assert response.status_code == 200
    data = response.get_json()
    assert 'metrics' in data
    assert 'Healthcare' in data['metrics']['domain']


def test_analyze_endpoint_upload_xlsx(client):
    excel_path = DATA_DIR / 'maritime_defense_vessel.xlsx'
    with excel_path.open('rb') as f:
        file_bytes = f.read()

    data = {
        'files': (io.BytesIO(file_bytes), 'maritime_defense_vessel.xlsx')
    }
    response = client.post('/api/analyze', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    res_data = response.get_json()
    assert 'metrics' in res_data
    assert 'Maritime & Defense' in res_data['metrics']['domain']


def test_api_test_key_endpoint_missing_key(client):
    response = client.post('/api/ai/test-key', json={'provider': 'gemini', 'api_key': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert data['ok'] is False
