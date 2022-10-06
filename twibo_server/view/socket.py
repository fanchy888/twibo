from twibo_server import socketIO


@socketIO.on('connect', namespace='/twibo')
def test_connect():
    print('connected')


@socketIO.on('auto_reply', namespace='/twibo')
def auto_reply(message):
    print(message)
    socketIO.emit('message', message[::-1], namespace='/twibo')

