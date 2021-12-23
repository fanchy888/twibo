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
    def create(cls, data):
        name = data['name']
        email = data['email']
        passwd = data['password']
        passwd = rsa_decrypt(passwd)
        if UserModel.check_name(name):
            raise ParameterError(400, f'User {name} already exists')
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
