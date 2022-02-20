
from sqlalchemy import INTEGER, VARCHAR, Boolean, Column, UniqueConstraint
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base


class FriendModel(Base, MixinBase):
    __tablename__ = 'Friend'

    friend_id = Column(INTEGER, primary_key=True, autoincrement=True)
    user_id = Column(VARCHAR(32), nullable=False)
    friend_user_id = Column(VARCHAR(32), nullable=False)
    nick_name = Column(VARCHAR(32))
    __table_args__ = (UniqueConstraint('user_id', 'friend_user_id', name='_friend_uc'),)

    @classmethod
    def get_friend(cls, user_id, friend_user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.user_id == user_id, cls.friend_user_id == friend_user_id).one_or_none()

    @classmethod
    def check_friendship(cls, user_id, friend_user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.user_id == user_id, cls.friend_user_id == friend_user_id).one_or_none()

    @classmethod
    def create_friendship(cls, request, receive):
        with session_manager() as session:
            model1 = cls(**request)
            model2 = cls(**receive)
            session.add(model1)
            session.add(model2)
            session.commit()

    @classmethod
    def delete_friend(cls, user_id, friend_user_id):
        with session_manager() as session:
            model1 = session.query(cls).filter(cls.user_id == user_id, cls.friend_user_id == friend_user_id).one_or_none()
            model2 = session.query(cls).filter(cls.user_id == friend_user_id, cls.friend_user_id == user_id).one_or_none()
            session.delete(model1)
            session.delete(model2)
            session.commit()


class FriendRequestModel(Base, MixinBase):
    __tablename__ = 'FriendRequest'

    request_id = Column(INTEGER, primary_key=True, autoincrement=True)
    from_user = Column(VARCHAR(32), nullable=False)
    to_user = Column(VARCHAR(32), nullable=False)
    active = Column(Boolean, default=True)

    @classmethod
    def get_one(cls, user_id, friend_user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.from_user == user_id, cls.to_user == friend_user_id).one_or_none()

    @classmethod
    def get_all(cls, user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.to_user == user_id).order_by(cls.create_time.desc()).all()
