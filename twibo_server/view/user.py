from flask import jsonify, g
from . import bp


@bp.route('/user', methods=['GET'])
def get_user():
    data = {'message': 'get user'}
    return jsonify(meta={'code': 200}, data=data)