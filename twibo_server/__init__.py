from datetime import timedelta
from flask import Flask, render_template
from flask_socketio import SocketIO
from twibo_server.config import config
from flask_mail import Mail, Message

import os

package_dir = os.path.dirname(os.path.abspath(__file__))
static = os.path.join(package_dir, "dist")

app = Flask(__name__, static_folder=static, template_folder=static)

app.config['SECRET_KEY'] = 'fcy'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

app.config['MAIL_SERVER'] = config.email_cfg['MAIL_SERVER']
app.config['MAIL_PORT'] = config.email_cfg['MAIL_PORT']
app.config['MAIL_USERNAME'] = config.email_cfg['MAIL_USERNAME']
app.config['MAIL_PASSWORD'] = config.email_cfg['MAIL_PASSWORD']
app.config['MAIL_USE_TLS'] = config.email_cfg['MAIL_USE_TLS']
app.config['MAIL_USE_SSL'] = config.email_cfg['MAIL_USE_SSL']
app.config['MAIL_DEFAULT_SENDER'] = config.email_cfg['MAIL_DEFAULT_SENDER']

mail = Mail()
mail.init_app(app)
socketIO = SocketIO(app, path="/socket-chat", cors_allowed_origins="*")

from twibo_server.view import bp
app.register_blueprint(bp)

