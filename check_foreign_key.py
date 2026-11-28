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
        'C999',
        '入院給付金',
        'テスト用の誤り',
        'テスト用の対応'
    ))

    raise RuntimeError('外部キー制約が機能していません')

except sqlite3.IntegrityError as e:
    if 'FOREIGN KEY' in str(e):
        print('登録が拒否されました:', e)
    else:
        raise

except sqlite3.Error as e:
    print('外部キー制約の確認エラー:', e)
    raise

finally:
    if conn is not None:
        conn.rollback()
        conn.close()