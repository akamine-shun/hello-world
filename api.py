from fastapi import FastAPI

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