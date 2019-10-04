#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from os import environ


@app_views.route('/projects/<project_id>/tasks', methods=['GET'])
def tasks_per_project(project_id=None):
    """
        reviews route to handle http method for requested reviews by project
    """
    project_obj = storage.get('Project', project_id)
    if request.method == 'GET':
        if project_obj is None:
            abort(404, 'Not found')
        all_tasks = storage.all('Task')
        project_tasks = project_obj.tasks
        project_tasks = [
            obj.to_json() for obj in project_tasks
            ]
        return jsonify(project_tasks)


@app_views.route('/projects/<project_id>/tasks/<task_id>',
                 methods=['DELETE', 'POST'])
def task_to_project(project_id=None, task_id=None):
    """
        reviews route to handle http methods for given review by ID
    """
    project_obj = storage.get('Project', project_id)
    task_obj = storage.get('Task', task_id)
    if project_obj is None:
        abort(404, 'Not found')
    if task_obj is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if (task_obj not in project_obj.tasks and
                task_obj.id not in project_obj.tasks):
            abort(404, 'Not found')
        project_obj.tasks.remove(task_obj)
        project_obj.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if (task_obj in project_obj.tasks or
                task_obj.id in project_obj.tasks):
            return jsonify(task_obj.to_json()), 200
        project_obj.tasks.append(task_obj)
        return jsonify(task_obj.to_json()), 201
