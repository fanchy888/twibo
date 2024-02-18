from datetime import datetime
from sqlalchemy import INTEGER, VARCHAR, BOOLEAN, TEXT, DateTime, Column, JSON
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base
from twibo_server.model.user import UserModel


class BlogModel(Base, MixinBase):
    __tablename__ = 'Blog'

    ARTICLE = 'article'

    blog_id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(64), nullable=False)
    content = Column(TEXT)
    author = Column(VARCHAR(32))
    abstract = Column(VARCHAR(256))
    content_type = Column(VARCHAR(32), default=ARTICLE)

    @classmethod
    def get(cls, blog_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.blog_id == blog_id).one_or_none()

    @classmethod
    def get_total_cnt(cls, keyword=''):
        with session_manager() as session:
            return session.query(cls).filter(cls.title.contains(keyword)).count()

    @classmethod
    def get_blogs(cls, keyword, limit=None, offset=None):
        with session_manager() as session:
            q = session.query(cls).order_by(cls.create_time.desc())
            if keyword:
                q = q.filter(cls.title.contains(keyword))
            if limit:
                q = q.limit(limit)
            if offset:
                q = q.offset(offset*limit)
            return q.all()

    @classmethod
    def get_stats(cls, blog_id):
        with session_manager() as session:
            count = session.query(CommentModel).filter(CommentModel.blog_id == blog_id,
                                                       CommentModel.comment_type == CommentModel.PLAIN).count()
            likes = session.query(CommentModel).filter(CommentModel.blog_id == blog_id,
                                                       CommentModel.comment_type == CommentModel.LIKE).count()
            votes = session.query(CommentModel).filter(CommentModel.blog_id == blog_id,
                                                       CommentModel.comment_type == CommentModel.VOTE).count()
            return {
                'count': count,
                'likes': likes,
                'votes': votes
            }

    def to_json(self):
        return {
            'blog_id': self.blog_id,
            'title': self.title,
            'author': self.author,
            'content': self.content,
            'abstract': self.abstract,
            'content_type': self.content_type,
            'time': self.create_time.timestamp(),
            'update_time': self.update_time.timestamp()
        }


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

    @classmethod
    def get_all(cls, blog_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.blog_id == blog_id).order_by(cls.create_time.desc()).all()

    @classmethod
    def delete_all(cls, blog_id):
        with session_manager() as session:
            session.query(cls).filter(cls.blog_id == blog_id).delete()

