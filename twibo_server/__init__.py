from datetime import timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO
from twibo_server.config import config

import os

package_dir = os.path.dirname(os.path.abspath(__file__))
static = os.path.join(package_dir, "dist")

app = Flask(__name__, static_folder=static, template_folder=static)

app.config['SECRET_KEY'] = 'fcy'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

socketIO = SocketIO(app, path="/socket-chat", cors_allowed_origins="*")

from twibo_server.view import bp
app.register_blueprint(bp)


@app.route('/')
def index():
    return render_template('twibo.html')