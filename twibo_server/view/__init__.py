from flask import Blueprint


bp = Blueprint('twibo', __name__, url_prefix='/api')

from . import user
from . import socket
