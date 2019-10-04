#!/usr/bin/python3
"""
Flask route that returns json status response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC
from os import environ


@app_views.route('/users/<user_id>/corrections', methods=['GET'])
def corrections_per_user(user_id=None):
    """
        reviews route to handle http method for requested reviews by user
    """
    user_obj = storage.get('User', user_id)
    if request.method == 'GET':
        if user_obj is None:
            abort(404, 'Not found')
        all_corrections = storage.all('Correction')
        user_corrections = user_obj.corrections
        user_corrections = [
            obj.to_json() for obj in user_corrections
            ]
        return jsonify(user_corrections)


@app_views.route('/users/<user_id>/corrections/<correction_id>',
                 methods=['DELETE', 'POST'])
def correction_to_user(user_id=None, correction_id=None):
    """
        reviews route to handle http methods for given review by ID
    """
    user_obj = storage.get('User', user_id)
    correction_obj = storage.get('Correction', correction_id)
    if user_obj is None:
        abort(404, 'Not found')
    if correction_obj is None:
        abort(404, 'Not found')

    if request.method == 'DELETE':
        if (correction_obj not in user_obj.corrections and
                correction_obj.id not in user_obj.corrections):
            abort(404, 'Not found')
        user_obj.corrections.remove(correction_obj)
        user_obj.save()
        return jsonify({}), 200

    if request.method == 'POST':
        if (correction_obj in user_obj.corrections or
                correction_obj.id in user_obj.corrections):
            return jsonify(correction_obj.to_json()), 200
        user_obj.corrections.append(correction_obj)
        return jsonify(correction_obj.to_json()), 201
