import os

from flask import Flask

app = Flask(__name__)
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'db.sqlite3'),
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

from app import routes

__all__ = ['routes', 'app']
