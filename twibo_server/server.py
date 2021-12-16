from flask import Flask, jsonify
from flask_socketio import SocketIO


app = Flask(__name__)
socketIO = SocketIO(app, cors_allowed_origins="*")


@app.route('/api/users', methods=['GET'])
def get_user():
    return jsonify({'code': 200, 'data': 'hello'})


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


if __name__ == '__main__':
    socketIO.run(app)
