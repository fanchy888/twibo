from flask import Flask
from flask_socketio import SocketIO
from sqlalchemy import create_engine
from twibo_server.config import config

app = Flask(__name__)
socketIO = SocketIO(app, cors_allowed_origins="*")
engine = create_engine(config.sqldb_url)

