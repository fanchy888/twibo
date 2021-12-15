from flask import Flask, jsonify
from flask_socketio import SocketIO
import random


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route('/api/users', methods=['GET'])
def get_user():
    return jsonify({'code': 200, 'data': 'hello'})


@socketio.on('connect', namespace='/test_conn')
def test_connect():
    while True:
        socketio.sleep(5)
        t = random_int_list(1, 100, 10)
        socketio.emit('server_response',
                      {'data': t},
                      namespace='/test_conn')


@socketio.on('test_input', namespace='/test_conn')
def test_input(message):
    # do someting
    socketio.emit('test_received', '收到啦', namespace='/test_conn')


def random_int_list(start, stop, length):
    start, stop = (int(start), int(stop)) if start <= stop else (int(stop), int(start))
    length = int(abs(length)) if length else 0
    random_list = []
    for i in range(length):
        random_list.append(random.randint(start, stop))
    return random_list


if __name__ == '__main__':
    socketio.run(app)
