import os

from flask import Flask

application = Flask(__name__)
app = application
POSTGRES = {
    'user': os.environ['RDS_USERNAME'],
    'password': os.environ['RDS_PASSWORD'],
    'database': os.environ['RDS_DB_NAME'],
    'host': os.environ['RDS_HOSTNAME'],
    'port': os.environ['RDS_PORT'],
}

application.config.update(dict(
    DATABASE=POSTGRES,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


from datetime import datetime
import psycopg2

from flask import request, g, jsonify, render_template

def connect_db():
    """Connects to the specific database."""
    rv = psycopg2.connect(**app.config['DATABASE'])
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.execute(f.read())


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
        g.sqlite_db.autocommit=True
        init_db()
    cursor = g.sqlite_db.cursor()
    return cursor


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/log')
def log():
    db = get_db()
    db.execute(
        'SELECT water_level,entry_time FROM entries ORDER BY entry_time DESC')
    return render_template("log.html", entries=db)


@app.route('/add', methods=['POST'])
def add_record():
    data = request.get_json(force=True)
    db = get_db()
    entry_value = round(data['level'] * 4) / 4.0
    time = datetime.now()
    db.execute(
        "INSERT INTO entries (water_level, entry_time)"
        "VALUES (?, ?)", [entry_value, time.isoformat()])
    return jsonify({"level": entry_value, "time": time})


@app.route('/last_level')
def last_level():
    db = get_db()
    cur = db.execute(
        'SELECT water_level FROM entries ORDER BY entry_time DESC LIMIT 1')
    for row in db:
        return str(row[0]*100) + "%  [" + "#" * int((row[0]*10)) + "-" * int(10-(row[0]*10)) + "]"
    return jsonify(0.0)


@app.route("/status")
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
    last = 0
    total = 0
    for row in db:
        if last > 0 and int(row[0]) == 0:
            total += 1
        last = row[0]
    return str((total/4.0)*100) + "%  [" + "#" * int((total/4)*10) + "-" * int(10-((total/4)*10)) + "]"

if __name__ == "__main__":
    application.run()
