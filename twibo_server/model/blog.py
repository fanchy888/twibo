from datetime import datetime
from sqlalchemy import INTEGER, VARCHAR, BOOLEAN, TEXT, DateTime, Column, JSON
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base
from twibo_server.model.user import UserModel


class BlogModel(Base, MixinBase):
    __tablename__ = 'Blog'

    blog_id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(64), nullable=False)
    content = Column(TEXT)
    author = Column(VARCHAR(32))
    abstract = Column(VARCHAR(256))
    like = Column(INTEGER)


class CommentModel(Base, MixinBase):
    __tablename__ = 'Comment'

    PLAIN = 'plain'
    LIKE = 'like'
    VOTE = 'vote'

    comment_id = Column(INTEGER, primary_key=True, autoincrement=True)
    content = Column(VARCHAR(256))
    author = Column(VARCHAR(32))
    parent_id = Column(INTEGER)
    blog_id = Column(INTEGER)
    comment_type = Column(VARCHAR(32), default=PLAIN)
