
from sqlalchemy import INTEGER, VARCHAR, BOOLEAN, TEXT, DateTime, Column, JSON
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base
from twibo_server.model.chat import ChatMemberModel


class GroupModel(Base, MixinBase):
    __tablename__ = 'Group'

    group_id = Column(VARCHAR(64), primary_key=True)
    chat_id = Column(INTEGER)
    name = Column(VARCHAR(32))
    description = Column(VARCHAR(64))
    avatar = Column(VARCHAR(128))
    creator = Column(VARCHAR(64))
    manager = Column(JSON)

    @classmethod
    def get(cls, group_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.group_id == group_id).one_or_none()

    @classmethod
    def get_by_chat_id(cls, chat_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.chat_id == chat_id).one_or_none()

    @classmethod
    def get_groups(cls, user_id):
        with session_manager() as session:
            return session.query(cls).join(ChatMemberModel, ChatMemberModel.chat_id == cls.chat_id
                                           ).filter(ChatMemberModel.user_id == user_id).all()

    def to_json(self):
        return {
            'group_id': self.group_id,
            'chat_id': self.chat_id,
            'name': self.name,
            'description': self.description,
            'avatar': self.avatar,
            'creator': self.creator,
            'manager': self.manager
        }