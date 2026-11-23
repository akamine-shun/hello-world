import sqlite3

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

conn.close()