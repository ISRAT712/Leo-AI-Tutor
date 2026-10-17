
import sqlite3
from datetime import datetime

DB_NAME = "leo.db"


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def save_quiz_result(topic, score, total):
    percentage = (score / total * 100) if total else 0

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO quiz_history
        (topic, score, total, percentage, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        topic,
        score,
        total,
        percentage,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def get_quiz_history():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM quiz_history
        ORDER BY id DESC
    """)

    results = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return results


create_table()
