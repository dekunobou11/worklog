import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'data.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # users テーブル
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # memos テーブル
    cur.execute('''
        CREATE TABLE IF NOT EXISTS memos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            content TEXT NOT NULL,
            tag TEXT,
            image TEXT,
            created_at TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ データベース初期化完了")

if __name__ == '__main__':
    init_db()