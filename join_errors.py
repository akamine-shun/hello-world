import sqlite3

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

conn.close()