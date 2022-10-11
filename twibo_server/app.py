from twibo_server import socketIO, app


if __name__ == '__main__':
    socketIO.run(app, debug=True, host='0.0.0.0')
