import os.path

from twibo_server.config import config
from twibo_server.model.user import UserModel
from twibo_server.model.friend import FriendModel, FriendRequestModel
from twibo_server.lib.uchat import ChatRoom, Message
from twibo_server.lib.exception import ParameterError
from twibo_server.utils import rsa_decrypt, generate_id, create_avatar, generate_pwd
from twibo_server import socketIO
from twibo_server.lib.tools import send_email


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
        account = data['account']
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
            'account': account,
            'email': email,
            'user_id': user_id
        }
        model = UserModel(**user)
        model.save()
        return user_id

    @classmethod
    def login(cls, data):
        account = data['account']
        passwd = data['password']
        passwd = rsa_decrypt(passwd)
        user = UserModel.get_by_account(account)
        if not user:
            raise ParameterError(400, 'User Account does not exist')
        if not user.check_password(passwd):
            raise ParameterError(400, 'Incorrect Password')

        data = user.to_json()
        # todo: optimize generate token
        data['token'] = user.user_id
        return data

    @classmethod
    def reset_password(cls, data):
        account = data['account']
        email = data['email']
        user = UserModel.get_by_account(account)
        if not user:
            raise ParameterError(400, 'Account does not exist')
        if user.email != email:
            raise ParameterError(400, 'Incorrect Email address ')
        else:
            password = generate_pwd()
            user.password = password
            user.save()

            content = f'''
            <p>Your new password has been set as: <p> 
            <h1>{password}<h1>
            '''
            send_email('reset password', content, email)

    @classmethod
    def upload_file(cls, file, data):
        base_path = config.static_url
        file_type = data['type']
        user_id = data['user_id']
        suffix = file.filename.split('.')[-1]
        file_name = file.filename
        if file_type == 'avatar':
            if suffix not in config.img_type:
                raise ParameterError(400, f'不支持文件格式 .{suffix}')
            file_name = f'avatar-{user_id}.{suffix}'
            user = UserModel.get(user_id)
            user.avatar = file_name
            user.save()
            file_path = os.path.join(base_path, file_name)

            file_content = file.read()
            thumbnail = create_avatar(file_content)
            thumbnail.save(file_path)

    def update_info(self, data):
        name = data['name']
        description = data['description']
        email = data['email']
        if UserModel.check_duplicate_name(name, self.user_id):
            raise ParameterError(400, f'User {name} has already existed')
        self.model.name = name
        self.model.description = description
        self.model.email = email
        self.model.save()

    def change_password(self, old, new):
        old = rsa_decrypt(old)
        new = rsa_decrypt(new)
        if not self.model.check_password(old):
            raise ParameterError(400, 'Password incorrect')
        self.model.password = new
        self.model.save()

    def get_friends(self):
        friend_models = UserModel.get_friends(self.user_id)

        friend_info = []
        for user, friend in friend_models:
            res = user.to_json()
            res['nick_name'] = friend.nick_name or user.name
            res['friend_id'] = friend.friend_id
            friend_info.append(res)
        friend_info.sort(key=lambda x: x['nick_name'].lower())
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
            request_model = FriendRequestModel(**data)
        request_model.save()
        msg = {
            'receiver': friend_user_id,
            'sender': self.model.to_json(),
        }
        socketIO.emit('requestFriend', msg, namespace='/twibo')

    def confirm_friend(self, user_id):
        request_model = FriendRequestModel.get_one(user_id, self.user_id)
        if request_model:
            request_model.active = False
            request_model.save()
        else:
            raise ParameterError(400, 'Request not found')
        request_model = FriendRequestModel.get_one(self.user_id, user_id)
        if request_model:
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
        if not FriendModel.check_friendship(self.user_id, user_id):
            FriendModel.create_friendship(from_user, to_user)

        chat_id = ChatRoom.create([self.user_id, user_id])

        socketIO.emit('clearRequest', [self.user_id, user_id], namespace='/twibo')
        socketIO.emit('createChat', [self.user_id, user_id], namespace='/twibo')
        self.say_hi(chat_id)

    def reject_friend(self, user_id):
        request_model = FriendRequestModel.get_one(user_id, self.user_id)
        if not request_model:
            return
        request_model.active = False
        request_model.save()

    def get_friend_requests(self):
        res = []
        for u in UserModel.get_friend_requests(self.user_id):
            res.append(u.to_json())
        return res

    def update_friend(self, friend_id, data):
        nick_name = data['nick_name']
        friend = FriendModel.get_friend(self.user_id, friend_id)
        if friend:
            friend.nick_name = nick_name
            friend.save()
        else:
            raise ParameterError(400, 'Friend not found')

    def delete_friend(self, friend_user_id):
        FriendModel.delete_friend(self.user_id, friend_user_id)
        ChatRoom.delete_chat([self.user_id, friend_user_id])

    def say_hi(self, chat_id):
        msg = {
            'sender': self.user_id,
            'chat_id': chat_id,
            'content': 'hi~'
        }
        Message.create(msg, False)

    def send_msg(self, msg):
        Message.create(msg)
        ChatRoom(msg['chat_id']).user_active(self.user_id)
