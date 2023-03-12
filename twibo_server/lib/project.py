from twibo_server.lib.exception import ParameterError
from twibo_server.lib.user import User
from twibo_server.model.project import ProjectModel, ProjectTaskModel


class Project:
    def __init__(self, project_id):
        self.project_id = project_id
        self._model = None
        self._tasks = []

    @property
    def model(self):
        if not self._model:
            model = ProjectModel.get(self.project_id)
            self._model = model
            if not model:
                raise ParameterError(400, 'project not found!')
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def __getattr__(self, item):
        return getattr(self.model, item)

    @property
    def owner(self):
        return User(self.model.owner)

    @property
    def tasks(self):
        if not self._tasks:
            self._tasks = ProjectTaskModel.get_tasks(self.project_id)
        return self._tasks

    @classmethod
    def get_by_owner(cls, user_id):
        projects = []
        for p in ProjectModel.get_by_user(user_id):
            pro = p.to_json()
            tasks = ProjectTaskModel.get_tasks(p.project_id)
            pro['tasks'] = [{'title': t.title, 'task_id': t.task_id, 'progress': t.progress} for t in tasks]
            projects.append(pro)
        return projects

    def get_project_info(self, user_id):
        if user_id != self.model.owner:
            raise ParameterError(400, 'No Access!')
        info = self.model.to_json()
        info['tasks'] = self.get_tasks()
        return info

    @classmethod
    def create(cls, data, user_id):
        if data['owner'] != user_id:
            raise ParameterError(400, 'No Access!')
        name = data['name']
        if ProjectModel.check_name(name, user_id):
            raise ParameterError(400, f'Project "{name}" already exists')
        data['owner'] = user_id
        ProjectModel(**data).save()

    def update(self, name, theme):
        self.model.name = name
        self.model.theme = theme
        self.model.save()

    def delete(self):
        ProjectTaskModel.delete_by_project(self.project_id)
        self.model.delete()

    def get_tasks(self):
        return [t.to_json() for t in self.tasks]

    def create_task(self, task_info):
        task_info['project_id'] = self.project_id
        ProjectTask.create(task_info)


class ProjectTask:
    def __init__(self, project_id, task_id):
        self.project_id = project_id
        self.task_id = task_id
        self._model = None

    @property
    def model(self):
        if not self._model:
            model = ProjectTaskModel.get(self.task_id)
            self._model = model
            if not model:
                raise ParameterError(400, 'task not found!')
        return self._model

    @model.setter
    def model(self, model):
        self._model = model

    def __getattr__(self, item):
        return getattr(self.model, item)

    @classmethod
    def create(cls, task_data):
        ProjectTaskModel(**task_data).save()

    def update(self, title, content):
        self.model.title = title
        self.model.content = content

    def archive(self):
        self.model.archived = True
        self.model.save()

    def delete(self):
        self.model.delete()
