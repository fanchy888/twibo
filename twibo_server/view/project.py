from flask import jsonify, g, request, session, abort
from . import bp, login_required
from twibo_server import socketIO
from twibo_server.lib.user import User
from twibo_server.lib.project import Project, ProjectTask
from twibo_server.utils import logger


@bp.route('/projects', methods=['GET'])
@login_required
def get_projects():
    user_id = g.user_id
    data = Project.get_by_owner(user_id)
    return jsonify(meta={'code': 200}, data=data)


@bp.route('/projects/<project_id>', methods=['GET'])
@login_required
def get_project(project_id):
    data = Project(project_id).get_project_info(g.user_id)
    return jsonify(meta={'code': 200}, data=data)


@bp.route('/projects', methods=["POST"])
@login_required
def create_project():
    user_id = g.user_id
    data = request.get_json()
    Project.create(data, user_id)
    return jsonify(meta={'code': 200}, data=data)


@bp.route('/projects/<project_id>', methods=['PATCH'])
@login_required
def update_project(project_id):
    params = request.get_json()
    name = params['name']
    theme = params['theme']
    Project(project_id).update(name, theme)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/projects/<project_id>', methods=['DELETE'])
@login_required
def delete_project(project_id):
    Project(project_id).delete()
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/projects/<project_id>/tasks', methods=['GET'])
@login_required
def get_tasks(project_id):
    tasks = Project(project_id).get_tasks()
    return jsonify(meta={'code': 200}, data=tasks)


@bp.route('/projects/<project_id>/tasks', methods=['POST'])
@login_required
def create_task(project_id):
    data = request.get_json()
    Project(project_id).create_task(data)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/projects/<project_id>/tasks/<task_id>', methods=['PATCH'])
@login_required
def update_task(project_id, task_id):
    data = request.get_json()
    title = data['title']
    content = data['content']
    ProjectTask(project_id, task_id).update(title, content)
    return jsonify(meta={'code': 200}, data={'success': True})


@bp.route('/projects/<project_id>/tasks/<task_id>', methods=['DELETE'])
@login_required
def delete_task(project_id, task_id):
    ProjectTask(project_id, task_id).delete()
    return jsonify(meta={'code': 200}, data={'success': True})





