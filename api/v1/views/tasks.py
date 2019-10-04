#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/tasks/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/tasks_no_id.yml', methods=['GET', 'POST'])
def tasks_no_id(task_id=None):
    """
        tasks route that handles http requests with no ID given
    """

    if request.method == 'GET':
        all_tasks = storage.all('Task')
        all_tasks = [obj.to_json() for obj in all_tasks.values()]
        return jsonify(all_tasks)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('title') is None:
            abort(400, 'Missing title')
        if req_json.get('project_id') is None:
            abort(400, 'Missing project id')
        Task = CNC.get('Task')
        new_object = Task(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/tasks/<task_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/tasks_id.yml', methods=['GET', 'DELETE', 'PUT'])
def task_with_id(task_id=None):
    """
        tasks route that handles http requests with ID given
    """
    task_obj = storage.get('Task', task_id)
    if task_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(task_obj.to_json())

    if request.method == 'DELETE':
        task_obj.delete()
        del task_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        task_obj.bm_update(req_json)
        return jsonify(task_obj.to_json()), 200
