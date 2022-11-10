from flask import jsonify, g, request, session, abort
from . import bp, login_required
from twibo_server.utils import logger


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
    session['user_id'] = user['user_id']
    return jsonify(meta={'code': 200}, data=user)


@bp.route('/password', methods=['POST'])
def reset_password():
    data = request.get_json()
    User.reset_password(data)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/logout', methods=['GET'])
@login_required
def logout():
    if session.get('user_id'):
        session.pop('user_id')
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/user', methods=['GET'])
@login_required
def get_user_info():
    user_id = request.args.get('user_id')
    user = User.get_user(user_id)
    return jsonify(meta={'code': 200}, data=user)


@bp.route('/user', methods=['PATCH'])
@login_required
def update_user_info():
    user_id = request.args.get('user_id')
    if g.user_id != user_id:
        abort(400, 'No Access!')
    data = request.get_json()
    User(user_id).update_info(data)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('file')
    data = dict(request.form)
    User.upload_file(file, data)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/user/search', methods=['GET'])
@login_required
def search_by_name():
    name = request.args.get('name')
    user = User(g.user_id).search_friend_by_name(name)
    return jsonify(meta={'code': 200}, data=user)


@bp.route('/user/<user_id>/friend', methods=['POST'])
@login_required
def add_friend(user_id):
    User(g.user_id).request_friend(user_id)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/user/<user_id>/friend/confirm', methods=['PATCH'])
@login_required
def confirm_friend(user_id):
    friend = request.args.get('friend_id')
    User(g.user_id).confirm_friend(friend)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/user/<user_id>/friend/reject', methods=['PATCH'])
@login_required
def reject_friend(user_id):
    friend = request.args.get('friend_id')
    User(g.user_id).reject_friend(friend)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/user/<user_id>/friends', methods=['GET'])
@login_required
def get_friends(user_id):
    friends = User(g.user_id).get_friends()
    return jsonify(meta={'code': 200}, data=friends)


@bp.route('/user/<user_id>/friend-request', methods=['GET'])
@login_required
def get_friend_request(user_id):
    req = User(g.user_id).get_friend_requests()
    return jsonify(meta={'code': 200}, data=req)


@bp.route('/user/<user_id>/friend/<friend_user_id>', methods=['PATCH'])
@login_required
def update_friend_info(user_id, friend_user_id):
    data = request.get_json()
    User(g.user_id).update_friend(friend_user_id, data)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/user/<user_id>/friend/<friend_user_id>', methods=['DELETE'])
@login_required
def delete_friend(user_id, friend_user_id):
    data = request.get_json()
    User(g.user_id).delete_friend(friend_user_id)
    return jsonify(meta={'code': 200}, data={'success': True})
