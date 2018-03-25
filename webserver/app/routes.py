# coding=utf-8
import sqlite3
from datetime import datetime

from flask import request, g, jsonify, render_template

from . import app


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


@app.route('/last_level')
def last_level():
    db = get_db()
    cur = db.execute(
        'SELECT water_level FROM entries ORDER BY entry_time DESC LIMIT 1')
    entries = cur.fetchall()
    for row in entries:
        return str(row[0]*100) + "%  [" + "#" * int((row[0]*10)) + "-" * int(10-(row[0]*10)) + "]"
    return jsonify(0.0)


@app.route("/")
def status():
    return render_template("progress.html", progress=last_level())


@app.route("/bottles_completed")
def bottles_completed():
    begin = datetime.now().replace(hour=0, minute=0, second=0)
    end = datetime.now().replace(hour=23, minute=59, second=59)
    epoch = datetime.utcfromtimestamp(0)
    db = get_db()
    cur = db.execute(
        'SELECT water_level FROM entries '
        #'WHERE entry_time > ? and entry_time < ? '
        'ORDER BY entry_time ASC') #[(begin - epoch).total_seconds() * 1000.0, (end - epoch).total_seconds() * 1000.0])
    entries = cur.fetchall()
    last = 0
    total = 0
    for row in entries:
        if last > 0 and int(row[0]) == 0:
            total += 1
        last = row[0]
    return str((total/4.0)*100) + "%  [" + "#" * int((total/4)*10) + "-" * int(10-((total/4)*10)) + "]"


