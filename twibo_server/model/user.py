from sqlalchemy import INTEGER, VARCHAR, Boolean, Column, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base
from twibo_server.model.friend import FriendModel, FriendRequestModel


class UserModel(Base, MixinBase):
    __tablename__ = 'User'

    user_id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    email = Column(VARCHAR(64), nullable=False, unique=True)  # register account
    _password_hash_ = Column(VARCHAR(256), nullable=False)
    avatar = Column(VARCHAR(128))
    description = Column(VARCHAR(64))
    system_admin = Column(Boolean, default=False)

    @classmethod
    def get(cls, user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.user_id == user_id).one_or_none()

    @classmethod
    def get_by_email(cls, email):
        with session_manager() as session:
            return session.query(cls).filter(cls.email == email).one_or_none()

    @classmethod
    def get_by_name(cls, name):
        with session_manager() as session:
            return session.query(cls).filter(cls.name == name).one_or_none()

    @property
    def password(self):
        raise Exception('Unable to get password')

    @password.setter
    def password(self, value):
        self._password_hash_ = generate_password_hash(str(value))

    def check_password(self, passwd):
        return check_password_hash(self._password_hash_, str(passwd))

    @classmethod
    def check_name(cls, name):
        with session_manager() as session:
            return bool(session.query(cls.name).filter(cls.name == name).all())

    @classmethod
    def check_email(cls, email):
        with session_manager() as session:
            return bool(session.query(cls.email).filter(cls.email == email).all())

    @classmethod
    def check_duplicate_name(cls, name, user_id):
        with session_manager() as session:
            return bool(session.query(cls.name).filter(cls.user_id != user_id, cls.name == name).all())

    @classmethod
    def get_users(cls, user_ids):
        with session_manager() as session:
            return session.query(cls).filter(cls.user_id.in_(user_ids)).all()

    @classmethod
    def get_friends(cls, user_id):
        with session_manager() as session:
            return session.query(cls, FriendModel).join(cls, FriendModel.friend_user_id == cls.user_id).filter(
                FriendModel.user_id == user_id).all()

    @classmethod
    def get_friend_requests(cls, user_id):
        with session_manager() as session:
            return session.query(cls).join(
                FriendRequestModel, FriendRequestModel.from_user == cls.user_id).filter(
                FriendRequestModel.to_user == user_id, FriendRequestModel.active.is_(True)).order_by(
                FriendRequestModel.create_time.desc()).all()

    def to_json(self):
        data = {
            'name': self.name,
            'user_id': self.user_id,
            'email': self.email,
            'avatar': self.avatar,
            'description': self.description,
            'system_admin': self.system_admin
        }
        return data
