import csv
import sqlite3

conn = None

try:
    conn = sqlite3.connect('kyufukin.db')
    conn.execute('PRAGMA foreign_keys = ON')
    cursor = conn.cursor()

    with open('kyufukin_sample.csv', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)

        for row in reader:
            cursor.execute('''
                INSERT INTO claims
                (claim_id, claim_amount, status)
                VALUES (?, ?, ?)
                ON CONFLICT(claim_id) DO UPDATE SET
                    claim_amount = excluded.claim_amount,
                    status = excluded.status
            ''', (
                row['claim_id'],
                int(row['claim_amount']),
                row['status']
            ))

    conn.commit()

    print('CSVデータを登録・更新しました')

except (sqlite3.Error, OSError, ValueError, KeyError) as e:
    if conn is not None:
        conn.rollback()

    print('CSVデータの登録・更新エラー:', e)
    raise

finally:
    if conn is not None:
        conn.close()