import sqlite3
from typing import Literal

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel

app = FastAPI()


class AssessmentError(BaseModel):
    claim_id: str
    claim_type: str
    error_detail: str
    correct_action: str


@app.get('/')
def home():
    return {'message': '給付金データ分析API'}


@app.get('/summary', summary='給付金の支払状況を集計')
def summary():
    conn = None

    try:
        conn = sqlite3.connect('kyufukin.db')
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT status, COUNT(*), SUM(claim_amount)
            FROM claims
            GROUP BY status
        ''')

        results = cursor.fetchall()

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail='データベース集計エラー'
        )

    finally:
        if conn is not None:
            conn.close()

    return {'summary': results}


@app.get('/claims', summary='給付金の支払状況を検索')
def get_claims(
    status: Literal['支払済', '審査中', '不支払'],
    min_amount: int = Query(default=0, ge=0)
):
    conn = None

    try:
        conn = sqlite3.connect('kyufukin.db')
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()

        try:
            cursor.execute('''
                SELECT claim_id, claim_amount, status
                FROM claims
                WHERE status = ? AND claim_amount >= ?
            ''', (status, min_amount))

            results = cursor.fetchall()

        except sqlite3.Error:
            raise HTTPException(
                status_code=500,
                detail='データベース検索エラー'
            )

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail='データベース接続エラー'
        )

    finally:
        if conn is not None:
            conn.close()

    claims = []

    for row in results:
        claims.append({
            'claim_id': row[0],
            'claim_amount': row[1],
            'status': row[2]
        })

    return {'claims': claims}


@app.get('/statistics', summary='給付金のデータの統計分析')
def get_statistics():
    conn = None

    try:
        conn = sqlite3.connect('kyufukin.db')
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                COUNT(*),
                AVG(claim_amount),
                MAX(claim_amount),
                MIN(claim_amount),
                SUM(CASE WHEN status = '支払済' THEN 1 ELSE 0 END)
            FROM claims
        ''')

        result = cursor.fetchone()

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail='データベース集計エラー'
        )

    finally:
        if conn is not None:
            conn.close()

    return {
        'total_claims': result[0],
        'average_amount': result[1],
        'max_amount': result[2],
        'min_amount': result[3],
        'paid_rate': result[4] / result[0] if result[0] > 0 else 0
    }


@app.get('/errors', summary='査定誤り事例を検索')
def get_errors(claim_type: str):
    conn = None

    try:
        conn = sqlite3.connect('kyufukin.db')
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT claim_id, claim_type, error_detail, correct_action
            FROM assessment_errors
            WHERE claim_type = ?
        ''', (claim_type,))

        results = cursor.fetchall()

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail='査定誤り事例の検索エラー'
        )

    finally:
        if conn is not None:
            conn.close()

    errors = []

    for row in results:
        errors.append({
            'claim_id': row[0],
            'claim_type': row[1],
            'error_detail': row[2],
            'correct_action': row[3]
        })

    return {'errors': errors}


@app.post('/errors', summary='査定誤り事例を登録', status_code=201)
def create_error(error: AssessmentError):
    conn = None

    try:
        conn = sqlite3.connect('kyufukin.db')
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()

        cursor.execute(
            'SELECT claim_id FROM claims WHERE claim_id = ?',
            (error.claim_id,)
        )

        if cursor.fetchone() is None:
            raise HTTPException(
                status_code=404,
                detail='案件番号が存在しません'
            )

        cursor.execute('''
            INSERT INTO assessment_errors
            (claim_id, claim_type, error_detail, correct_action)
            VALUES (?, ?, ?, ?)
        ''', (
            error.claim_id,
            error.claim_type,
            error.error_detail,
            error.correct_action
        ))

        conn.commit()

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail='査定誤りの事例の登録エラー'
        )

    finally:
        if conn is not None:
            conn.close()

    return {'message': '査定誤りの事例を登録しました'}


@app.get('/errors/details', summary='査定誤り事例と給付金情報を取得')
def get_error_details():
    conn = None

    try:
        conn = sqlite3.connect('kyufukin.db')
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                c.claim_id,
                c.claim_amount,
                c.status,
                e.claim_type,
                e.error_detail,
                e.correct_action
            FROM claims AS c
            INNER JOIN assessment_errors AS e
                ON c.claim_id = e.claim_id
        ''')

        results = cursor.fetchall()

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail='査定誤り詳細情報の取得エラー'
        )

    finally:
        if conn is not None:
            conn.close()

    details = []

    for row in results:
        details.append({
            'claim_id': row[0],
            'claim_amount': row[1],
            'status': row[2],
            'claim_type': row[3],
            'error_detail': row[4],
            'correct_action': row[5]
        })

    return {'details': details}