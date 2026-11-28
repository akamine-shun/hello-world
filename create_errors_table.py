import sqlite3

conn = None

try:
    conn = sqlite3.connect('kyufukin.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()

    cursor.execute('BEGIN')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS claims (
            claim_id TEXT NOT NULL,
            claim_amount INTEGER,
            status TEXT
        )
    ''')

    cursor.execute('''
        CREATE UNIQUE INDEX IF NOT EXISTS
        idx_claims_claim_id ON claims(claim_id)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS assessment_errors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim_id TEXT NOT NULL,
            claim_type TEXT NOT NULL,
            error_detail TEXT NOT NULL,
            correct_action TEXT,
            FOREIGN KEY (claim_id)
                REFERENCES claims(claim_id)
        )
    ''')

    conn.commit()

    print('給付金・査定誤り管理テーブルを作成しました')

except sqlite3.Error as e:
    if conn is not None:
        conn.rollback()

    print('テーブル作成エラー:', e)
    raise

finally:
    if conn is not None:
        conn.close()