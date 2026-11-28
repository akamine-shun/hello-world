import sqlite3

conn = None

try:
    conn = sqlite3.connect('kyufukin.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO assessment_errors
        (claim_id, claim_type, error_detail, correct_action)
        VALUES (?, ?, ?, ?)
    ''', (
        'C001',
        '入院給付金',
        '入院日数の計算誤り',
        '支払対象日数を再確認する'
    ))

    conn.commit()

    print('査定誤り事例を登録しました')

except sqlite3.Error as e:
    if conn is not None:
        conn.rollback()

    print('査定誤り事例の登録エラー:', e)
    raise

finally:
    if conn is not None:
        conn.close()