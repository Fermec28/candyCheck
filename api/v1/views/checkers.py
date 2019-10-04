#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/checks/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/checks_no_id.yml', methods=['GET', 'POST'])
def checks_no_id(check_id=None):
    """
        checks route that handles http requests with no ID given
    """

    if request.method == 'GET':
        all_checks = storage.all('Check')
        all_checks = [obj.to_json() for obj in all_checks.values()]
        return jsonify(all_checks)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('title') is None:
            abort(400, 'Missing title')
        if req_json.get('passed') is None:
            abort(400, 'Missing passed')
        if req_json.get('correction_id') is None:
            abort(400, 'Missing correction id')
        Check = CNC.get('Check')
        new_object = Check(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/checks/<check_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/checks_id.yml', methods=['GET', 'DELETE', 'PUT'])
def check_with_id(check_id=None):
    """
        checks route that handles http requests with ID given
    """
    check_obj = storage.get('Check', check_id)
    if check_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(check_obj.to_json())

    if request.method == 'DELETE':
        check_obj.delete()
        del check_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        check_obj.bm_update(req_json)
        return jsonify(check_obj.to_json()), 200
