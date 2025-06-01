# utils/auth.py
from functools import wraps
from flask import session, redirect, url_for, request
import sqlite3
import os
import hashlib
from flask import current_app, g

def get_db():
    if 'db' not in g:
        db_path = os.path.join(current_app.root_path, 'data.db')
        g.db = sqlite3.connect(db_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def validate_user(username, password):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    return user and user['password'] == hash_password(password)

def register_user(username, password):
    db = get_db()
    existing = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if existing:
        return False
    db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
    db.commit()
    return True

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function