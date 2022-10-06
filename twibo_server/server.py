from twibo_server import socketIO, app
from twibo_server.view import bp

app.register_blueprint(bp)

if __name__ == '__main__':
    socketIO.run(app, debug=True, host='0.0.0.0')
