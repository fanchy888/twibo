import os
from twibo_server.model.group import GroupModel
from twibo_server.lib.uchat import ChatRoom
from twibo_server.lib.user import User
from twibo_server.model.chat import ChatRoomModel, ChatMemberModel
from twibo_server.lib.exception import ParameterError
from twibo_server.config import config
from twibo_server.utils import logger
from twibo_server import socketIO
from twibo_server.utils import generate_id, create_avatar


class Group:
    def __init__(self, group_id):
        self.group_id = group_id
        self._model = None

    @property
    def model(self):
        if not self._model:
            model = GroupModel.get(self.group_id)
            self._model = model
            if not model:
                raise ParameterError(400, 'group not found!')
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def __getattr__(self, item):
        return getattr(self.model, item)

    @classmethod
    def creator_name(cls, creator):
        return User(creator).name

    @classmethod
    def create_group(cls, creator, data, avatar=None):
        members = data['members']
        if len(members) < 3:
            raise ParameterError(400, 'Group must contain at least 3 members')
        chat_info = {

            'name': data['name'],
            'description': data['description'],
            'chat_type': ChatRoomModel.GROUP
        }
        chat_id = ChatRoomModel.create_chat(**chat_info)
        for user_id in members:
            member = {
                'chat_id': chat_id,
                'user_id': user_id,
            }
            ChatMemberModel(**member).save()
        group_id = generate_id('group')
        group = {
            'group_id': group_id,
            'creator': data['creator'],
            'name': data['name'],
            'description': data['description'],
            'chat_id': chat_id,
            'manager': [],
        }
        GroupModel(**group).save()
        if avatar:
            cls(group_id).upload_avatar(avatar)
        creator.say_hi(chat_id, '三人成虎\nWelcome to this group.')
        socketIO.emit('createGroup', [m for m in members], namespace='/twibo')

        return group_id

    @classmethod
    def delete_group(cls, creator, group_id):
        group = GroupModel.get(group_id)
        if group.creator == creator:
            chat_id = group.chat_id
            ChatRoomModel.delete_chat(chat_id)
            group.delete()

    def edit_group(self, data):
        description = data.get('description')
        name = data.get('name')
        if name:
            self.model.name = name
        if description:
            self.model.description = description
        self.model.save()

    def upload_avatar(self, file):
        base_path = config.static_url
        suffix = file.filename.split('.')[-1]
        if suffix not in config.img_type:
            raise ParameterError(400, f'不支持文件格式 .{suffix}')

        file_content = file.read()
        thumbnail = create_avatar(file_content)
        name = self.group_id
        file_name = name + '.' + suffix
        file_path = os.path.join(base_path, file_name)
        thumbnail.save(file_path)
        self.model.avatar = file_name
        self.model.save()
        return file_name

    @classmethod
    def get_groups(cls, user_id):
        groups = GroupModel.get_groups(user_id)
        res = []
        for group in groups:
            group_info = group.to_json()
            chat_room = ChatRoom(group.chat_id)
            members = chat_room.get_members()

            group_info['members'] = members
            group_info['owner'] = cls.creator_name(group.creator)
            res.append(group_info)
        return res

    def get_group_info(self):
        info = self.model.to_json()
        chat_room = ChatRoom(self.chat_id)
        members = chat_room.get_members()
        info['members'] = members
        info['owner'] = self.creator_name(self.creator)
        return info

    def add_group_member(self, adder, user_ids):
        if not ChatMemberModel.get_member(self.chat_id, adder):
            raise ParameterError(400, 'You are not in this group')
        for user_id in user_ids:
            member = {
                'chat_id': self.chat_id,
                'user_id': user_id,
            }
            ChatMemberModel(**member).save()

    def kick_group_member(self, creator, user_id):
        if self.creator == user_id or self.creator != creator:
            return
        m = ChatMemberModel.get_member(self.chat_id, user_id)
        m.delete()
        socketIO.emit('kick', {'user_id': user_id, 'group': self.name},
                      to=self.chat_id, namespace='/twibo')
