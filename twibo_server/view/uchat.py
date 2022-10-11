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


@socketIO.on('chat', namespace='/twibo')
def chat(message):
    User(message['sender']).send_msg(message)


@socketIO.on('joinChat', namespace='/twibo')
def join_chat(data):
    user_id = data['user_id']
    chat_id = data['chat_id']
    ChatRoom(chat_id).join_user(user_id)