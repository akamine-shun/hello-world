from fastapi import FastAPI, Query, HTTPException
from typing import Literal

app = FastAPI()

@app.get('/')
def home():
    return {'message': '給付金データ分析API'}

import sqlite3

@app.get('/summary', summary='給付金の支払状況を集計')
def summary():
    conn = None

    try:
        conn = sqlite3.connect('kyufukin.db')
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
    try:
        conn = sqlite3.connect('kyufukin.db')
        cursor = conn.cursor()
    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail='データベース接続エラー'
        )
    try:
        cursor.execute(
            '''SELECT claim_id, claim_amount, status
            FROM claims
            WHERE status = ? AND claim_amount >= ?
            ''',
            (status, min_amount)
    )
    
        results = cursor.fetchall()

    except sqlite3.Error:
        raise HTTPException(
            status_code=500,
            detail='データベース検索エラー'
        )

    finally:
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