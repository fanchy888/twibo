from sqlalchemy import INTEGER, VARCHAR, Column, or_, UniqueConstraint
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base


class UserModel(Base, MixinBase):
    __tablename__ = 'User'

    user_id = Column(VARCHAR(32), primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    email = Column(VARCHAR(64), nullable=False, unique=True)  # register account
    password = Column(VARCHAR(32), nullable=False)
    avatar = Column(VARCHAR(128))


class FriendModel(Base, MixinBase):
    __tablename__ = 'Friend'

    friend_id = Column(INTEGER, primary_key=True, autoincrement=True)
    request_user = Column(VARCHAR(32), nullable=False)
    receive_user = Column(VARCHAR(32), nullable=False)
    __table_args__ = (UniqueConstraint('request_user', 'receive_user', name='_friend_uc'),)

    @classmethod
    def get_friend(cls, user_id):
        with session_manager() as session:
            requested = session.query(cls.receive_user).filter(cls.request_user == user_id)
            received = session.query(cls.request_user).filter(cls.receive_user == user_id)
            return received.union(requested).all()

