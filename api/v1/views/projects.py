#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/projects/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/projects_no_id.yml', methods=['GET', 'POST'])
def projects_no_id(project_id=None):
    """
        projects route that handles http requests with no ID given
    """

    if request.method == 'GET':
        all_projects = storage.all('Project')
        all_projects = [obj.to_json() for obj in all_projects.values()]
        return jsonify(all_projects)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('name') is None:
            abort(400, 'Missing name')
        Project = CNC.get('Project')
        new_object = Project(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/projects/<project_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/projects_id.yml', methods=['GET', 'DELETE', 'PUT'])
def project_with_id(project_id=None):
    """
        projects route that handles http requests with ID given
    """
    project_obj = storage.get('Project', project_id)
    if project_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(project_obj.to_json())

    if request.method == 'DELETE':
        project_obj.delete()
        del project_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        project_obj.bm_update(req_json)
        return jsonify(project_obj.to_json()), 200
