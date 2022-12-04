from flask import jsonify, g, request, session, abort
from . import bp, login_required
from twibo_server import socketIO
from twibo_server.lib.user import User
from twibo_server.utils import logger


@bp.route('/blogs', method=['GET'])
@login_required
def get_blogs():
    target_user = request.args.get('user_id')
    blogs = []
    return jsonify(meta={'code': 200}, data=blogs)
