from fastapi import FastAPI, Query
from typing import Literal

app = FastAPI()

@app.get('/')
def home():
    return {'message': '給付金データ分析API'}

import sqlite3

@app.get('/summary', summary='給付金の支払状況を集計')
def summary():
    conn = sqlite3.connect('kyufukin.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT status, COUNT(*), SUM(claim_amount)
        FROM claims
        GROUP BY status
        ''')

    results = cursor.fetchall()
    conn.close()

    return {'summary': results}

@app.get('/claims', summary='給付金の支払状況を検索')
def get_claims(
    status: Literal['支払済', '審査中', '不支払'],
    min_amount: int = Query(default=0, ge=0)
    ):
    conn = sqlite3.connect('kyufukin.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        SELECT claim_id, claim_amount, status
        FROM claims
        WHERE status = ? AND claim_amount >= ?
        ''',
        (status, min_amount)
    )

    results = cursor.fetchall()
    conn.close()

    claims = []

    for row in results:
        claims.append({
            'claim_id': row[0],
            'claim_amount': row[1],
            'status': row[2]
        })

    return {'claims': claims}