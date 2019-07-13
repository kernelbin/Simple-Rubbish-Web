from flask import Flask
from flask_socketio import SocketIO
import config

app = Flask("SimpleRubbish-Web")
socket = SocketIO(app)
