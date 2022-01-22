
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
    def get_friends(cls, user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.user_id == user_id).all()
