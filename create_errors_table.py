import sqlite3

conn = sqlite3.connect('kyufukin.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS assessment_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    claim_id TEXT NOT NULL,
    claim_type TEXT NOT NULL,
    error_detail TEXT NOT NULL,
    correct_action TEXT
    )
    ''')

conn.commit()
conn.close()

print('査定誤り管理テーブルを作成しました')