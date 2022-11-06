from flask import jsonify, g, request, session, abort
from . import bp, login_required
from twibo_server import socketIO
from twibo_server.lib.uchat import ChatRoom
from twibo_server.lib.user import User
from twibo_server.utils import logger


@bp.route('/chats', methods=['GET'])
def get_chats():
    user = User(g.user_id)
    rooms = ChatRoom.get_chat_room(user)
    return jsonify(meta={'code': 200}, data=rooms)


@bp.route('/chats/<chat_id>/img', methods=['POST'])
def upload_img(chat_id):
    file_list = request.files.getlist("file")
    user = User(g.user_id)
    info = ChatRoom(chat_id).send_imgs(user, file_list)
    return jsonify(meta={'code': 200}, data=info)


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
