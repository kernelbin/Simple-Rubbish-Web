from main import socket, app, config
socket.run(app, host=config.HOST, port=config.PORT, debug=config.DEBUG)
