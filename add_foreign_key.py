import sqlite3

conn = None

try:
    conn = sqlite3.connect('kyufukin.db')
    cursor = conn.cursor()

    cursor.execute('PRAGMA foreign_keys = ON')
    cursor.execute('BEGIN')

    cursor.execute('''
        CREATE TABLE assessment_errors_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            claim_id TEXT NOT NULL,
            claim_type TEXT NOT NULL,
            error_detail TEXT NOT NULL,
            correct_action TEXT,
            FOREIGN KEY (claim_id)
                REFERENCES claims(claim_id)
        )
    ''')

    cursor.execute('''
        INSERT INTO assessment_errors_new
        (id, claim_id, claim_type, error_detail, correct_action)
        SELECT id, claim_id, claim_type, error_detail, correct_action
        FROM assessment_errors
    ''')

    cursor.execute('DROP TABLE assessment_errors')

    cursor.execute('''
        ALTER TABLE assessment_errors_new
        RENAME TO assessment_errors
    ''')

    conn.commit()

    print('外部キー制約を設定しました')

except sqlite3.Error as e:
    if conn is not None:
        conn.rollback()

    print('外部キー制約の設定エラー:', e)
    raise

finally:
    if conn is not None:
        conn.close()