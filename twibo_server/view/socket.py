from twibo_server import socketIO


@socketIO.on('connect', namespace='/test_conn')
def test_connect():
    print('connected')


@socketIO.on('connect1', namespace='/test_conn')
def test_connect():
    print('connected1')


@socketIO.on('message', namespace='/test_conn')
def test_input(message):
    # do someting
    print(message)
    socketIO.emit('received', '收到啦', namespace='/test_conn')


@socketIO.on('auto_reply', namespace='/test_conn')
def auto_reply(message):
    print(message)
    socketIO.emit('message', message[::-1], namespace='/test_conn')

