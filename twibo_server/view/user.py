from flask import jsonify, g, request, abort
from . import bp
from .extentions import login_required

from twibo_server.lib.user import User


@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_id = User.create(data)
    return jsonify(meta={'code': 200}, data={'user-id': user_id})


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.login(data)
    return jsonify(meta={'code': 200}, data=user)


@bp.route('/user', methods=['GET'])
@login_required
def get_user():
    args = request.args
    user_id = args['user_id']
    return jsonify(meta={'code': 200}, data={'user-name': User(user_id).name})