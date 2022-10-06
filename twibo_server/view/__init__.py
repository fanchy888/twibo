from functools import wraps
from flask import Blueprint, g, request, jsonify, session


bp = Blueprint('twibo', __name__, url_prefix='/api')


@bp.after_request
def after_request(response):
    from twibo_server.model.mysql_manager import clear_session
    clear_session()
    return response


@bp.before_request
def before_request():
    g.user_id = session.get('user_id')


def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authentication')  # user_id
        user_id = session.get('user_id')
        if not token or not user_id or token != user_id:
            return jsonify(meta={'code': 401}, data={'msg': 'Login Required'})
        return func(*args, **kwargs)
    return decorator


from . import user
from . import socket
from . import uchat
