from twibo_server.model.chat import ChatRoomModel, ChatMessageModel
from twibo_server.lib.exception import ParameterError
from twibo_server.utils import rsa_decrypt, generate_id
from twibo_server import socketIO
from twibo_server.config import config
from twibo_server.lib.user import User


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

    def members(self):
        for user, _, member in ChatRoomModel.get_members(self.chat_id):
            member_info = user.to_json()
            member_info['last_read'] = member.last_read.strftime("%Y%m%d %H%M%S")


class Message:
    def __init__(self):
        pass
