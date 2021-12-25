from sqlalchemy import INTEGER, VARCHAR, Boolean, Column, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base


class UserModel(Base, MixinBase):
    __tablename__ = 'User'

    user_id = Column(VARCHAR(32), primary_key=True)
    name = Column(VARCHAR(32), nullable=False, unique=True)
    email = Column(VARCHAR(64), nullable=False, unique=True)  # register account
    _password_hash_ = Column(VARCHAR(256), nullable=False)
    avatar = Column(VARCHAR(128))
    system_admin = Column(Boolean, default=False)

    @classmethod
    def get(cls, user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.user_id == user_id).one_or_none()

    @classmethod
    def get_by_email(cls, email):
        with session_manager() as session:
            return session.query(cls).filter(cls.email == email).one_or_none()

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

    def to_json(self):
        data = {
            'name': self.name,
            'user_id': self.user_id,
            'email': self.email,
            'avatar': self.avatar,
            'system_admin': self.system_admin
        }
        return data


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

