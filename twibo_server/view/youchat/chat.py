from twibo_server import socketIO


@socketIO.on('chat', namespace='/twibo')
def chat():
    pass