import os

import dateutil
from datetime import datetime
from flask import Flask

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.sqlite3'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))


def format_datetime(value, format='medium'):
    if format == 'full':
        format = "EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format = "EE dd.MM.y HH:mm"
    try:
        return datetime.strptime(format, value)
    except AttributeError:
        return datetime.strptime(dateutil.parser.parse(format, value))


app.jinja_env.filters['datetime'] = format_datetime

from app import routes

__all__ = ['routes', 'app']
