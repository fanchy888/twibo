
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
        if not self._model:
            self.model = UserModel.get(self.user_id)
        return getattr(self.model, item)

    @classmethod
    def get_user(cls, user_id):
        return UserModel.get(user_id)

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
