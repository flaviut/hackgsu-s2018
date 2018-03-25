# coding=utf-8
import sqlite3
from datetime import datetime

from flask import request, g, jsonify, render_template

from app import app


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/log')
def log():
    db = get_db()
    cur = db.execute(
        'SELECT water_level,entry_time FROM entries ORDER BY entry_time DESC')
    return render_template("log.html", entries=cur.fetchall())


@app.route('/add', methods=['POST'])
def add_record():
    data = request.get_json(force=True)
    db = get_db()
    entry_value = round(data['level'] * 4) / 4.0
    time = datetime.now()
    db.execute(
        "INSERT INTO entries (water_level, entry_time)"
        "VALUES (?, ?)", [entry_value, time.isoformat()])
    db.commit()
    return jsonify({"level": entry_value, "time": time})
