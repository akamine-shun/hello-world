import sqlite3
from unittest.mock import patch

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

def test_statistics_db_error():
    with patch(
        'api.sqlite3.connect',
        side_effect=sqlite3.OperationalError('接続失敗')
    ):
        response = client.get('/statistics')

    assert response.status_code == 500
    assert response.json()['detail'] == 'データベース集計エラー'

def test_summary_db_error():
    with patch(
        'api.sqlite3.connect',
        side_effect=sqlite3.OperationalError('接続失敗')
    ):
        response = client.get('/summary')

    assert response.status_code == 500
    assert response.json()['detail'] == 'データベース集計エラー'

def test_claims_db_error():
    with patch(
        'api.sqlite3.connect',
        side_effect=sqlite3.OperationalError('接続失敗')
    ):
        response = client.get(
            '/claims',
            params={'status': '支払済', 'min_amount': 0}
        )

    assert response.status_code == 500
    assert response.json()['detail'] == 'データベース接続エラー'

def test_errors():
    response = client.get(
        '/errors',
        params={'claim_type': '入院給付金'}
    )

    assert response.status_code == 200

    data = response.json()

    assert 'errors' in data
    assert len(data['errors']) >= 1
    assert data['errors'][0]['claim_type'] == '入院給付金'

def test_errors_db_error():
    with patch(
        'api.sqlite3.connect',
        side_effect=sqlite3.OperationalError('接続失敗')
    ):
        response = client.get(
            '/errors',
            params={'claim_type': '入院給付金'}
        )

    assert response.status_code == 500
    assert response.json()['detail'] == '査定誤り事例の検索エラー'