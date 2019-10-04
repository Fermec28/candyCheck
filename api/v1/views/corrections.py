#!/usr/bin/python3
"""
    Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from flasgger.utils import swag_from


@app_views.route('/corrections/', methods=['GET', 'POST'])
@swag_from('swagger_yaml/corrections_no_id.yml', methods=['GET', 'POST'])
def corrections_no_id(correction_id=None):
    """
        corrections route that handles http requests with no ID given
    """

    if request.method == 'GET':
        all_corrections = storage.all('Correction')
        all_corrections = [obj.to_json() for obj in all_corrections.values()]
        return jsonify(all_corrections)

    if request.method == 'POST':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        if req_json.get('status') is None:
            abort(400, 'Missing status')
        if req_json.get('user_id') is None:
            abort(400, 'Missing user id')
        if req_json.get('project_id') is None:
            abort(400, 'Missing project id')
        Correction = CNC.get('Correction')
        new_object = Correction(**req_json)
        new_object.save()
        return jsonify(new_object.to_json()), 201


@app_views.route('/corrections/<correction_id>', methods=['GET', 'DELETE', 'PUT'])
@swag_from('swagger_yaml/corrections_id.yml', methods=['GET', 'DELETE', 'PUT'])
def correction_with_id(correction_id=None):
    """
        corrections route that handles http requests with ID given
    """
    correction_obj = storage.get('Correction', correction_id)
    if correction_obj is None:
        abort(404, 'Not found')

    if request.method == 'GET':
        return jsonify(correction_obj.to_json())

    if request.method == 'DELETE':
        correction_obj.delete()
        del correction_obj
        return jsonify({}), 200

    if request.method == 'PUT':
        req_json = request.get_json()
        if req_json is None:
            abort(400, 'Not a JSON')
        correction_obj.bm_update(req_json)
        return jsonify(correction_obj.to_json()), 200
