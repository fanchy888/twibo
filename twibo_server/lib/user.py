import os.path

from twibo_server.config import config
from twibo_server.model.user import UserModel
from twibo_server.model.friend import FriendModel, FriendRequestModel
from twibo_server.lib.exception import ParameterError
from twibo_server.utils import rsa_decrypt, generate_id
from twibo_server import socketIO


class User:
    def __init__(self, user_id):
        self.user_id = user_id
        self._model = None

    @property
    def model(self):
        if not self._model:
            model = UserModel.get(self.user_id)
            self._model = model
            if not model:
                raise ParameterError(400, 'user not found!')
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def __getattr__(self, item):
        return getattr(self.model, item)

    @classmethod
    def get_user(cls, user_id):
        user = UserModel.get(user_id)
        if not user:
            raise ParameterError(400, 'User not found')
        return user.to_json()

    @classmethod
    def create(cls, data):
        name = data['name']
        email = data['email']
        passwd = data['password']
        passwd = rsa_decrypt(passwd)
        if UserModel.check_name(name):
            raise ParameterError(400, f'User {name} has already existed')
        if UserModel.check_email(email):
            raise ParameterError(400, f'Account {email} has already been used')
        user_id = generate_id('user')

        user = {
            'name': name,
            'password': passwd,
            'email': email,
            'user_id': user_id
        }
        model = UserModel(**user)
        model.save()
        return user_id

    @classmethod
    def login(cls, data):
        email = data['email']
        passwd = data['password']
        passwd = rsa_decrypt(passwd)
        user = UserModel.get_by_email(email)
        if not user:
            raise ParameterError(400, 'User Account does not exist')
        if not user.check_password(passwd):
            raise ParameterError(400, 'Password incorrect')

        data = user.to_json()
        # todo: optimize generate token
        data['token'] = user.user_id
        return data

    @classmethod
    def upload_file(cls, file, data):
        base_path = config.static_path
        file_type = data['type']
        user_id = data['user_id']
        suffix = file.filename.split('.')[-1]
        file_name = file.filename
        if file_type == 'avatar':
            if suffix not in config.avatar_type:
                raise ParameterError(400, f'不支持文件格式 .{suffix}')
            file_name = f'avatar-{user_id}.{suffix}'
            user = UserModel.get(user_id)
            user.avatar = file_name
            user.save()
        file_path = os.path.join(base_path, file_name)
        file.save(file_path)

    def update_info(self, data):
        name = data['name']
        description = data['description']
        if not UserModel.check_duplicate_name(name, self.user_id):
            raise ParameterError(400, f'User {name} has already existed')
        self.model.name = name
        self.model.description = description
        self.model.save()

    def get_friends(self):
        friend_models = FriendModel.get_friends(self.user_id)

        nick_names = {f.user_id: f.nick_name for f in friend_models}
        friends_list = UserModel.get_users(list(nick_names.keys()))
        friend_info = []
        for f in friends_list:
            res = f.to_json()
            res['nick_name'] = nick_names[f.user_id]
            friend_info.append(res)
        return friend_info

    def search_friend_by_name(self, name):
        user = UserModel.get_by_name(name)
        if user:
            if user.user_id == self.user_id or FriendModel.check_friendship(self.user_id, user.user_id):
                user = None
            else:
                user = user.to_json()
        return user

    def request_friend(self, friend_user_id):
        request_model = FriendRequestModel.get_one(self.user_id, friend_user_id)
        if request_model:
            request_model.active = True
        else:
            data = {
                'from_user': self.user_id,
                'to_user': friend_user_id,
            }
            request_model = FriendRequestModel()
        request_model.save()
        msg = {
            'receiver': friend_user_id,
            'sender': self.model.to_json(),
        }
        socketIO.emit('requestFriend', msg, namespace='/twibo')

    def confirm_friend(self, user_id):
        request_model = FriendRequestModel.get_one(user_id, self.user_id)
        if not request_model:
            raise ParameterError(400, 'No friendship request found')
        request_model.active = False
        request_model.save()
        from_user = {
            'user_id': user_id,
            'friend_user_id': self.user_id
        }
        to_user = {
            'user_id': self.user_id,
            'friend_user_id': user_id
        }
        FriendModel.create_friendship(from_user, to_user)
