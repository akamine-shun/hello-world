import sqlite3

conn = sqlite3.connect('kyufukin.db')
cursor = conn.cursor()

cursor.execute('''
INSERT INTO assessment_errors
(claim_id, claim_type, error_detail, correct_action)
VALUES (?, ?, ?, ?)
''',(
    'A001',
    '入院給付金',
    '入院日数の計算誤り',
    '支払対象日数を再確認する'
))

conn.commit()
conn.close()

print('査定誤り事例を登録しました')