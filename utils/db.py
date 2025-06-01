# utils/db.py
import sqlite3
import os
from flask import g, current_app

def get_db():
    if 'db' not in g:
        db_path = os.path.join(current_app.root_path, 'data.db')
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def get_memos_by_user(username):
    db = get_db()
    return db.execute('SELECT * FROM memos WHERE username = ? ORDER BY created_at DESC', (username,)).fetchall()

def insert_memo(username, content, tags, image_filename):
    db = get_db()
    db.execute(
        'INSERT INTO memos (username, content, tag, image, created_at) VALUES (?, ?, ?, ?, datetime("now"))',
        (username, content, ', '.join(tags), image_filename)
    )
    db.commit()

def get_tags_by_user(username):
    db = get_db()
    rows = db.execute('SELECT tag FROM memos WHERE username = ?', (username,)).fetchall()
    tag_set = set()
    for row in rows:
        tag_list = [tag.strip() for tag in row['tag'].split(',') if tag.strip()]
        tag_set.update(tag_list)
    return sorted(list(tag_set))

def search_memos(username, keyword=None, tag=None, start=None, end=None):
    db = get_db()
    query = 'SELECT * FROM memos WHERE username = ?'
    params = [username]

    if keyword:
        query += ' AND content LIKE ?'
        params.append(f'%{keyword}%')

    if tag:
        query += ' AND tag LIKE ?'
        params.append(f'%{tag}%')

    if start:
        query += ' AND date(created_at) >= date(?)'
        params.append(start)

    if end:
        query += ' AND date(created_at) <= date(?)'
        params.append(end)

    query += ' ORDER BY created_at DESC'
    return db.execute(query, params).fetchall()

def update_memo(username, memo_id, content, tags):
    db = get_db()
    tag_string = ', '.join(tags)
    db.execute(
        'UPDATE memos SET content = ?, tag = ? WHERE id = ? AND username = ?',
        (content, tag_string, memo_id, username)
    )
    db.commit()

def get_memo_by_id(username, memo_id):
    db = get_db()
    return db.execute('SELECT * FROM memos WHERE id = ? AND username = ?', (memo_id, username)).fetchone()