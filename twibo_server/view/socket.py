from twibo_server import socketIO
from .extentions import login_required


@socketIO.on('connect', namespace='/twibo')
def test_connect():
    print('connected')


@socketIO.on('connect1', namespace='/twibo')
def test_connect():
    print('connected1')


@socketIO.on('message', namespace='/twibo')
def test_input(message):
    # do someting
    print(message)
    socketIO.emit('received', '收到啦', namespace='/twibo')


@socketIO.on('auto_reply', namespace='/twibo')
def auto_reply(message):
    print(message)
    socketIO.emit('message', message[::-1], namespace='/twibo')

