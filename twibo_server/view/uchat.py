from flask import jsonify, g, request, session, abort
from . import bp, login_required
from twibo_server import socketIO
from twibo_server.lib.uchat import ChatRoom
from twibo_server.lib.group import Group
from twibo_server.lib.user import User
from twibo_server.utils import logger


@socketIO.on('chat', namespace='/twibo')
def chat(message):
    User(message['sender']).send_msg(message)


@socketIO.on('read', namespace='/twibo')
def read_chat(data):
    user_id = data['user_id']
    chat_id = data['chat_id']
    ChatRoom(chat_id).user_active(user_id)


@socketIO.on('joinChat', namespace='/twibo')
def join_chat(user_id):
    ChatRoom.join_chats(user_id)


@socketIO.on('leaveChat', namespace='/twibo')
def leave_chat(data):
    ChatRoom.leave_chat(data['user_id'], data['chat_id'])


@bp.route('/chats', methods=['GET'])
def get_chats():
    user = User(g.user_id)
    rooms = ChatRoom.get_chat_room(user)
    return jsonify(meta={'code': 200}, data=rooms)


@bp.route('/chats/<chat_id>/img', methods=['POST'])
@login_required
def upload_img(chat_id):
    file_list = request.files.getlist("file")
    user = User(g.user_id)
    info = ChatRoom(chat_id).send_imgs(user, file_list)
    return jsonify(meta={'code': 200}, data=info)


@bp.route('/groups', methods=['GET'])
@login_required
def get_group_chat():
    groups = Group.get_groups(g.user_id)
    return jsonify(meta={'code': 200}, data=groups)


@bp.route('/groups', methods=['POST'])
@login_required
def create_group():
    members = request.form.getlist('members')
    name = request.form['name']
    description = request.form['description']
    creator = request.form['creator']
    if creator != g.user_id:
        abort(400, 'Access Denied')
    file = request.files.get('file')
    members.append(creator)
    data = {
        'members': members,
        'name': name,
        'description': description,
        'creator': creator
    }

    group_id = Group.create_group(User(creator), data, file)

    return jsonify(meta={'code': 200}, data={'group_id': group_id})


@bp.route('/groups/<group_id>/avatar', methods=['POST'])
@login_required
def upload_group_avatar(group_id):
    file = request.files.get('file')
    name = Group(group_id).upload_avatar(file)
    return jsonify(meta={'code': 200}, data={'avatar': name})


@bp.route('/groups/<group_id>', methods=['GET'])
def get_one_group(group_id):
    data = Group(group_id).get_group_info()
    return jsonify(meta={'code': 200}, data=data)


@bp.route('/groups/<group_id>', methods=['DELETE'])
@login_required
def delete_group_chat(group_id):
    Group.delete_group(g.user_id, group_id)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/groups/<group_id>', methods=['PATCH'])
@login_required
def edit_group_chat(group_id):
    data = request.get_json()
    Group(group_id).edit_group(data)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/groups/<group_id>/members', methods=['POST'])
@login_required
def add_group_member(group_id):
    data = request.get_json()
    Group(group_id).add_group_member(g.user_id, data)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/groups/<group_id>/members', methods=['PATCH'])
@login_required
def delete_group_member(group_id):
    data = request.get_json()
    Group(group_id).kick_group_members(g.user_id, data['user_ids'])
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/groups/<group_id>/members/<user_id>', methods=['DELETE'])
@login_required
def quit_group(group_id, user_id):
    if g.user_id != user_id:
        abort(400, 'Access Denied')
    Group(group_id).quit_group(user_id)
    return jsonify(meta={'code': 200}, data={'success': True})
