import csv
import sqlite3

conn = sqlite3.connect('kyufukin.db')
cursor = conn.cursor()

cursor.execute('DELETE FROM claims')

with open('kyufukin_sample.csv', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)

    for row in reader:
        cursor.execute(
            'INSERT INTO claims (claim_id, claim_amount, status) VALUES (?, ?, ?)',
            (row['claim_id'], int(row['claim_amount']), row['status'])
        )

conn.commit()
conn.close()

print('CSVデータを登録しました')