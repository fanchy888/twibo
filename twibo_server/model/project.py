from sqlalchemy import INTEGER, VARCHAR, Boolean, Column, TEXT
from twibo_server.model.mysql_manager import session_manager, MixinBase, Base
from twibo_server.model.friend import FriendModel, FriendRequestModel


class ProjectModel(Base, MixinBase):
    __tablename__ = 'Project'

    project_id = Column(INTEGER, autoincrement=True, primary_key=True)
    name = Column(VARCHAR(128), nullable=False)
    theme = Column(VARCHAR(512))
    owner = Column(VARCHAR(64), nullable=False)

    @classmethod
    def get(cls, project_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.project_id == project_id).one_or_none()

    @classmethod
    def check_name(cls, name, owner):
        with session_manager() as session:
            return session.query(cls).filter(cls.name == name, cls.owner == owner).one_or_none()

    @classmethod
    def get_by_user(cls, user_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.owner == user_id).all()

    def to_json(self):
        return {
            'project_id': self.project_id,
            'name': self.name,
            'theme': self.theme,
            'owner': self.owner,
            'create_date': self.create_time.timestamp()
        }


class ProjectTaskModel(Base, MixinBase):
    __tablename__ = 'ProjectTask'

    task_id = Column(INTEGER, autoincrement=True, primary_key=True)
    project_id = Column(INTEGER)
    archived = Column(Boolean, default=False)
    title = Column(VARCHAR(512))
    content = Column(TEXT)
    progress = Column(INTEGER, default=0)

    @classmethod
    def get(cls, task_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.task_id == task_id).one_or_none()

    @classmethod
    def get_tasks(cls, project_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.project_id == project_id).order_by(cls.create_time).all()

    @classmethod
    def delete_by_project(cls, project_id):
        with session_manager() as session:
            return session.query(cls).filter(cls.project_id == project_id).delete()

    def to_json(self):
        return {
            'task_id': self.task_id,
            'project_id': self.project_id,
            'archived': self.archived,
            'title': self.title,
            'content': self.content,
            'progress': self.progress,
            'create_date': self.create_time.timestamp()
        }
