from datetime import datetime
from sqlalchemy import INTEGER, VARCHAR, BOOLEAN, TEXT, DateTime, Column
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base
from twibo_server.model.user import UserModel


class ChatRoomModel(Base, MixinBase):
    __tablename__ = 'ChatRoom'

    PERSONAL = 'personal'
    GROUP = 'group'

    chat_id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(32))
    chat_type = Column(VARCHAR(16), default=PERSONAL)
    description = Column(VARCHAR(64))

    @classmethod
    def get(cls, chat_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.chat_id == chat_id).one_or_none()

    @classmethod
    def get_by_user(cls, user_id):
        with session_manager() as session:
            return session.query(ChatMemberModel).filter(ChatMemberModel.user_id == user_id).distinct().all()

    @classmethod
    def get_members(cls, chat_id):
        with session_manager() as session:
            return session.query(UserModel, cls, ChatMemberModel).join(
                    ChatMemberModel, ChatMemberModel.user_id == UserModel.user_id).join(
                        cls, cls.chat_id == ChatMemberModel.chat_id).filter(cls.chat_id == chat_id).all()

    @classmethod
    def get_chat_from_members(cls, user1, user2):
        with session_manager() as session:
            chat_ids = session.query(cls.chat_id).join(ChatMemberModel, cls.chat_id == ChatMemberModel.chat_id).filter(
                        ChatMemberModel.user_id == user1, cls.chat_type == cls.PERSONAL).all()
            chat_id = session.query(ChatMemberModel.chat_id).filter(ChatMemberModel.chat_id.in_([c[0] for c in chat_ids]),
                                                                    ChatMemberModel.user_id == user2).all()
            return chat_id and chat_id[0][0]

    @classmethod
    def delete_chat(cls, chat_id):
        with session_manager() as session:
            session.query(cls).filter(cls.chat_id == chat_id).delete()
            session.query(ChatMemberModel).filter(ChatMemberModel.chat_id == chat_id).delete()
            session.commit()

    @classmethod
    def create_chat(cls, **data):
        with session_manager() as session:
            model = cls(**data)
            session.add(model)
            session.flush()
            chat_id = model.chat_id
            session.commit()
            return chat_id


class ChatMemberModel(Base, MixinBase):
    __tablename__ = 'ChatMember'

    member_id = Column(INTEGER, primary_key=True, autoincrement=True)
    chat_id = Column(INTEGER)
    user_id = Column(VARCHAR(32), nullable=False)
    admin = Column(BOOLEAN, default=False)
    last_read = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_member(cls, chat_id, user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.chat_id == chat_id, cls.user_id == user_id).one_or_none()


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
    def get_by_chat_id(cls, chat_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.chat_id == chat_id).order_by(cls.create_time.asc()).all()

    def to_json(self):
        return {
            'msg_id': self.msg_id,
            'chat_id': self.chat_id,
            'sender': self.sender,
            'content': self.content,
            'type': self.content_type,
            'time': self.create_time.timestamp()
        }
