#!/usr/bin/env python3
"""Script for the hardware"""
import RPi.GPIO as GPIO  
import time
from flask import Flask, jsonify, make_response
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)


app = Flask(__name__)
app.url_map.strict_slashes = False

@app.route('/' )  
def hello():
	return("Hola")

@app.route("/status")
def status():
	message = { 'status' : "Verga, si esta funcionando el hardware" }
	return jsonify(message), 200

@app.route("/candy")
def candy():
	GPIO.output(12, True)
	time.sleep(2)	
	GPIO.output(12, False)
	message = { 'status' : "Candy delivered" }
	return jsonify(message), 200


@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port='5000')
