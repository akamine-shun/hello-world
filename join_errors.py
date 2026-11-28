import sqlite3

conn = None

try:
    conn = sqlite3.connect('kyufukin.db')
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

    for row in results:
        print(row)

except sqlite3.Error as e:
    print('査定誤り詳細情報の取得エラー:', e)
    raise

finally:
    if conn is not None:
        conn.close()