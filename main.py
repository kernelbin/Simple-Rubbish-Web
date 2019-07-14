

from flask import Flask, Blueprint
from flask_socketio import SocketIO
# import config
try:
    import config
except Exception:
    import config_default as config
from flask_wtf import CSRFProtect
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("SimpleRubbish-Web")
app.config["SQLALCHEMY_DATABASE_URI"] = config.DATABASE_URI
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config["DEBUG"] = config.DEBUG
app.secret_key = config.SESSION_KEY
basedir = os.path.dirname(__file__)
db = SQLAlchemy(app)
csrf=CSRFProtect(app)

socket = SocketIO(app)
# api = Blueprint("api","api")
# app.register_blueprint(api, url_prefix="/api")

from models import *
from routes import *