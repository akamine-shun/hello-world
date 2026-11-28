import sqlite3
import runpy
import shutil
from pathlib import Path

import pytest

def test_foreign_key(tmp_path, monkeypatch):
    project_dir = Path(__file__).resolve().parent

    monkeypatch.chdir(tmp_path)

    runpy.run_path(str(
        project_dir / 'create_errors_table.py'
    ))

    conn = sqlite3.connect('kyufukin.db')
    conn.execute('PRAGMA foreign_keys = ON')

    try:
        with pytest.raises(sqlite3.IntegrityError, match='FOREIGN KEY'):
            conn.execute('''
                INSERT INTO assessment_errors
                (claim_id, claim_type, error_detail, correct_action)
                VALUES (?, ?, ?, ?)
            ''', (
                'C999',
                '入院給付金',
                'テスト用の誤り',
                'テスト用の対応'
            ))

    finally:
        conn.rollback()
        conn.close()

def test_upsert(tmp_path, monkeypatch):
    project_dir = Path(__file__).resolve().parent

    monkeypatch.chdir(tmp_path)

    shutil.copy(
        project_dir / 'kyufukin_sample.csv',
        tmp_path / 'kyufukin_sample.csv'
    )

    runpy.run_path(str(
        project_dir / 'create_errors_table.py'
    ))

    runpy.run_path(str(
        project_dir / 'import_csv.py'
    ))

    conn = sqlite3.connect('kyufukin.db')

    try:
        conn.execute('''
            UPDATE claims
            SET claim_amount = 1
            WHERE claim_id = 'C001'
        ''')
        conn.commit()

        runpy.run_path(str(
            project_dir / 'import_csv.py'
        ))

        count = conn.execute(
            'SELECT COUNT(*) FROM claims'
        ).fetchone()[0]

        amount = conn.execute('''
            SELECT claim_amount FROM claims
            WHERE claim_id = 'C001'
        ''').fetchone()[0]

        assert count == 50
        assert amount == 56000

    finally:
        conn.close()