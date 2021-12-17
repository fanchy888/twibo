from flask import Flask
from flask_socketio import SocketIO


app = Flask(__name__)
socketIO = SocketIO(app, cors_allowed_origins="*")

