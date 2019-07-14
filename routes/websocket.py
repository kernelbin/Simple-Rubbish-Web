from main import socket
from flask_socketio import emit


@socket.on("echo")
def echo(data):
    emit("echo", data)
