#!/usr/bin/python3
"""
Flask route that returns json response
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage, CNC

@app_views.route('/correction/', methods=['GET', 'POST'])
def correction():
    """
        correction route that handles http
    """

    if request.method == 'GET':
        return "I'm here GET"

    if request.method == 'POST':
        return "I'm here POST"
