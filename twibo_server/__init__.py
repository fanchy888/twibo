from datetime import timedelta
from flask import Flask
from flask_socketio import SocketIO
from twibo_server.config import config

app = Flask(__name__, static_folder='dist')
app.config['SECRET_KEY'] = 'fcy'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

socketIO = SocketIO(app, cors_allowed_origins="*")

