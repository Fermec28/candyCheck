#!/usr/bin/python3
"""
Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC

@app_views.route('/project/', methods=['GET', 'POST'])
def project(user_id=None):
    """
        projects route that handles http
    """

    if request.method == 'GET':
        return "I'm here GET"

    if request.method == 'POST':
        return "I'm here POST"
