import sqlite3

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

    for row in results:
        print(row)

except sqlite3.Error as e:
    print('給付金データの集計エラー:', e)
    raise

finally:
    if conn is not None:
        conn.close()