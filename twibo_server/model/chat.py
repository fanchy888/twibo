from datetime import datetime
from sqlalchemy import INTEGER, VARCHAR, BOOLEAN, TEXT, DateTime, Column
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base
from twibo_server.model.user import UserModel


class ChatRoomModel(Base, MixinBase):
    __tablename__ = 'ChatRoom'

    PERSONAL = 'personal'
    GROUP = 'group'

    chat_id = Column(INTEGER, primary_key=True, autoincrement=True)
    chat_type = Column(VARCHAR(16), default=PERSONAL)
    description = Column(VARCHAR(64))

    @classmethod
    def get(cls, chat_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.chat_id == chat_id).one_or_none()

    @classmethod
    def get_members(cls, chat_id):
        with session_manager() as session:
            session.query(UserModel, cls, ChatMemberModel).join(
                ChatMemberModel, ChatMemberModel.user_id == UserModel.user_id).join(
                cls, cls.chat_id == ChatMemberModel.chat_id).filter(cls.chat_id == chat_id).all()


class ChatMemberModel(Base, MixinBase):
    __tablename__ = 'ChatMember'

    member_id = Column(INTEGER, primary_key=True, autoincrement=True)
    chat_id = Column(INTEGER)
    user_id = Column(VARCHAR(32), nullable=False)
    admin = Column(BOOLEAN)
    last_read = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ChatMessageModel(Base, MixinBase):
    __tablename__ = 'Message'

    TXT = 0
    PIC = 1
    VID = 2

    chat_id = Column(INTEGER)
    msg_id = Column(INTEGER, primary_key=True, autoincrement=True)
    sender = Column(VARCHAR(32), nullable=False)
    content = Column(TEXT)
    content_type = Column(INTEGER, default=TXT)

    @classmethod
    def get_by_char_id(cls, chat_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.char_id == chat_id).order_by(cls.create_time.acs()).all()

    def to_json(self):
        return {
            'chat_id': self.chat_id,
            'sender': self.sender,
            'content': self.content,
            'read': self.read
        }
