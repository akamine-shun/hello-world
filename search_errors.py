import sqlite3

conn = None

try:
    conn = sqlite3.connect('kyufukin.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT claim_id, claim_type, error_detail, correct_action
        FROM assessment_errors
        WHERE claim_type = ?
    ''', ('入院給付金',))

    results = cursor.fetchall()

    for row in results:
        print(row)

except sqlite3.Error as e:
    print('査定誤り事例の検索エラー:', e)
    raise

finally:
    if conn is not None:
        conn.close()