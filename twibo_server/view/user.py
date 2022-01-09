from flask import jsonify, g, request, session
from . import bp, login_required


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


@bp.route('/upload', methods=['POST'])
@login_required
def upload():
    file = request.files.get('file')
    data = dict(request.form)
    User.upload_file(file, data)
    return jsonify(meta={'code': 200}, data={'success': True})

