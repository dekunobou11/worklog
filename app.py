# app.py（編集機能対応）
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from werkzeug.utils import secure_filename
import os
import uuid
import markdown
from utils.auth import login_required, register_user, validate_user
from utils.db import get_memos_by_user, insert_memo, get_tags_by_user, search_memos, update_memo, get_memo_by_id
from utils.exporter import export_as_zip
from utils.markdown_parser import render_markdown

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.context_processor
def utility_processor():
    return dict(render_markdown=render_markdown)

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    username = session['username']
    if request.method == 'POST':
        content = request.form['content']
        tags = [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()]
        image_file = request.files.get('image')

        image_filename = None
        if image_file and image_file.filename:
            ext = os.path.splitext(image_file.filename)[1]
            image_filename = f"{uuid.uuid4().hex}__{secure_filename(image_file.filename)}"
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)

        insert_memo(username, content, tags, image_filename)
        return redirect(url_for('index'))

    keyword = request.args.get('keyword')
    tag = request.args.get('tag')
    start = request.args.get('start')
    end = request.args.get('end')

    memos = search_memos(username, keyword, tag, start, end)
    tags = get_tags_by_user(username)
    return render_template('index.html', memos=memos, tags=tags)

@app.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if validate_user(request.form['username'], request.form['password']):
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return render_template('login.html', error='ログインに失敗しました')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if register_user(request.form['username'], request.form['password']):
            return redirect(url_for('login'))
        return render_template('register.html', error='登録に失敗しました')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/export')
@login_required
def export():
    username = session['username']
    keyword = request.args.get('keyword')
    tag = request.args.get('tag')
    start = request.args.get('start')
    end = request.args.get('end')
    export_format = request.args.get('format')

    memos = search_memos(username, keyword, tag, start, end)
    return export_as_zip(memos, export_format)

@app.route('/edit_form/<int:memo_id>')
@login_required
def edit_memo_form(memo_id):
    username = session['username']
    memo = get_memo_by_id(username, memo_id)
    if memo is None:
        return redirect(url_for('index'))
    return render_template('edit.html', memo=memo)

@app.route('/edit_memo/<int:memo_id>', methods=['POST'])
@login_required
def edit_memo(memo_id):
    username = session['username']
    content = request.form['content']
    tags = [tag.strip() for tag in request.form.get('tags', '').split(',') if tag.strip()]
    update_memo(username, memo_id, content, tags)
    return redirect(url_for('index'))
