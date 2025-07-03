import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:////data/app.db")

def _db_path(url: str) -> str:
    if url.startswith("sqlite:///"):
        return url[len("sqlite:///") :]
    if url.startswith("sqlite:////"):
        return "/" + url[len("sqlite:////") :]
    return url

def get_db_connection():
    conn = sqlite3.connect(_db_path(DATABASE_URL))
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    conn.execute(
        'CREATE TABLE IF NOT EXISTS players ('
        'id INTEGER PRIMARY KEY AUTOINCREMENT,'
        'name TEXT UNIQUE NOT NULL,'
        'shots INTEGER NOT NULL DEFAULT 0'
        ')'
    )
    conn.commit()
    conn.close()

@app.before_first_request
def _init_db_if_needed():
    """Ensure the database schema exists before handling requests."""
    init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    players = conn.execute('SELECT * FROM players ORDER BY shots DESC, name').fetchall()
    conn.close()
    return render_template('index.html', players=players)

@app.route('/add_player', methods=['POST'])
def add_player():
    name = request.form['name'].strip()
    if name:
        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO players (name) VALUES (?)', (name,))
            conn.commit()
        except sqlite3.IntegrityError:
            pass  # ignore duplicate names
        conn.close()
    return redirect(url_for('index'))

@app.route('/increment/<int:player_id>', methods=['POST'])
def increment(player_id):
    conn = get_db_connection()
    conn.execute('UPDATE players SET shots = shots + 1 WHERE id = ?', (player_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
