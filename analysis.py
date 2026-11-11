import sqlite3

conn = sqlite3.connect('kyufukin.db')
cursor = conn.cursor()

cursor.execute('''
SELECT status, COUNT(*), SUM(claim_amount)
FROM claims
GROUP BY status
''')

results = cursor.fetchall()

for row in results:
    print(row)

conn.close()