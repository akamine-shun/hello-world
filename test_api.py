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

def test_statistics():
    response = client.get('/statistics')

    assert response.status_code == 200

    data = response.json()

    assert data['total_claims'] == 50
    assert data['average_amount'] >= 0
    assert data['max_amount'] >= data['min_amount']
    assert 0 <= data['paid_rate'] <= 1