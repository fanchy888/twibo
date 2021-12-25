from functools import wraps
from flask import request, jsonify

from twibo_server.lib.user import User


def login_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = request.headers.get('Authentication')  # user_id
        if not token or not User.get_user(token):
            return jsonify(meta={'code': 401}, data={'msg': 'Login Required'})
        return func(*args, **kwargs)
    return decorator

