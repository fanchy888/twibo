import os
import copy

from datetime import datetime
from twibo_server.model.chat import ChatRoomModel, ChatMessageModel, ChatMemberModel
from twibo_server.model.friend import FriendModel
from twibo_server.lib.exception import ParameterError
from twibo_server import socketIO
from twibo_server.config import config
from flask_socketio import join_room, rooms
from twibo_server.utils import logger
from twibo_server.utils import generate_id, create_thumbnail


class ChatRoom:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self._model = None

    @property
    def model(self):
        if not self._model:
            model = ChatRoomModel.get(self.chat_id)
            self._model = model
            if not model:
                raise ParameterError(400, 'chat room not found!')
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def __getattr__(self, item):
        return getattr(self.model, item)

    def get_members(self, exclude=None):
        members = []
        for user, _, member in ChatRoomModel.get_members(self.chat_id):
            if exclude and user.user_id == exclude:
                continue
            member_info = user.to_json()
            member_info['last_read'] = member.last_read.timestamp()
            members.append(member_info)
        return members

    def get_member_last_read(self, user_id):
        mem = ChatMemberModel.get_member(self.chat_id, user_id)
        return mem and mem.last_read.timestamp()

    @classmethod
    def get_chat_room_for_users(cls, users):
        if len(users) == 2:
            return ChatRoomModel.get_chat_from_friends(*users)
        else:
            # group chat
            return None

    @classmethod
    def create(cls, users):
        chat_id = cls.get_chat_room_for_users(users)
        if not chat_id:
            chat_id = ChatRoomModel.create_chat()
            for user_id in users:
                member = {
                    'chat_id': chat_id,
                    'user_id': user_id,
                }
                ChatMemberModel(**member).save()
        return chat_id

    @classmethod
    def delete_chat(cls, users):
        chat_id = cls.get_chat_room_for_users(users)
        if chat_id:
            ChatRoomModel.delete_chat(chat_id)

    @classmethod
    def get_chat_room(cls, user):
        chat_rooms = []
        user_id = user.user_id
        friend_list = user.get_friends()
        friends = {f['user_id']: f for f in friend_list}
        for chat in ChatRoomModel.get_by_user(user_id):
            chat_id = chat.chat_id
            chat_room = cls(chat_id)
            room_messages = Message(chat_id).get_messages()
            members = chat_room.get_members()
            for m in members:
                if m['user_id'] in friends:
                    m['name'] = friends[m['user_id']]['nick_name']
            last_seen = chat_room.get_member_last_read(user_id)

            if len(members) == 2:  # private
                others = [m for m in members if m['user_id'] != user_id][0]
                room = {
                    'name': others['name'],
                    'avatar': others['avatar'],
                    'user_id': others['user_id']
                }

            else:  # group
                room = {
                    'name': chat.name
                }

            room['members'] = members
            room['last_read'] = last_seen
            room['chat_id'] = chat_id
            room['messages'] = room_messages
            room['time'] = room_messages[-1]['time'] if room_messages else ''
            chat_rooms.append(room)
        chat_rooms = sorted(chat_rooms, key=lambda x: x['time'], reverse=True)
        return chat_rooms

    def user_active(self, user_id):
        m = ChatMemberModel.get_member(self.chat_id, user_id)
        m.last_read = datetime.utcnow()
        m.save()

    @classmethod
    def join_chats(cls, user_id):
        in_rooms = rooms(namespace='/twibo')
        for chat in ChatRoomModel.get_by_user(user_id):
            if chat.chat_id not in in_rooms:
                join_room(chat.chat_id, namespace='/twibo')
                logger.info(f'user{user_id} join room {chat.chat_id}')

    def send_imgs(self, user, files):
        msgs = []
        for file in files:
            file_name = self.save_img(file)
            data = {
                'sender': user.user_id,
                'chat_id': int(self.chat_id),
                'content': file_name,
                'content_type': ChatMessageModel.PIC
            }
            msgs.append(data)
        return msgs

    @staticmethod
    def save_img(file):
        base_path = config.img_url
        suffix = file.filename.split('.')[-1]
        if suffix not in config.img_type:
            raise ParameterError(400, f'不支持文件格式 .{suffix}')

        file_content = file.read()
        thumbnail = create_thumbnail(file_content)
        name = generate_id('img')

        file_name = name + '.' + suffix
        file_path = os.path.join(base_path, file_name)
        thumbnail.save(file_path)
        return file_name


class Message:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    @classmethod
    def create(cls, msg, send=True):
        sender = msg['sender']
        chat_id = msg['chat_id']
        content = msg['content']
        data = {
            'sender': sender,
            'chat_id': chat_id,
            'content': content,
            'content_type': msg.get('content_type', 0)
        }
        ChatMessageModel(**data).save()
        data['time'] = int(datetime.utcnow().timestamp())
        if send:
            socketIO.emit('chat', data, room=chat_id, namespace='/twibo')

    def get_messages(self):
        msgs = ChatMessageModel.get_by_chat_id(self.chat_id)
        return [m.to_json() for m in msgs]