import os.path

from twibo_server.config import config
from twibo_server.model.user import UserModel
from twibo_server.lib.exception import ParameterError
from twibo_server.utils import rsa_decrypt, generate_id


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
            raise ParameterError(400, f'Email has already been used')
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
            raise ParameterError(400, 'User email does not exist')
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