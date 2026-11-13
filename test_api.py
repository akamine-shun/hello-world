from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_home():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {
        'message': '給付金データ分析API'
    }

def test_summary():
    response = client.get('/summary')

    assert response.status_code == 200
    assert 'summary' in response.json()

def test_claims():
    response = client.get(
        '/claims',
        params={'status': '支払済', 'min_amount': 100000}
    )

    assert response.status_code == 200
    assert 'claims' in response.json()

def test_invalid_amount():
    response = client.get(
        '/claims',
        params={'status': '支払済', 'min_amount': -10000}
    )

    assert response.status_code == 422