#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, render_template, url_for, request, redirect
from models import storage
import uuid


# flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'


# begin flask page rendering
@app.teardown_appcontext
def teardown_db(exception):
    """
    after each request, this method calls .close() (i.e. .remove()) on
    the current SQLAlchemy Session
    """
    storage.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    handles request to custom template with states, cities & amentities
    """
    error = None
    if request.method == 'POST':
        if request.form['email'] != 'admin' or request.form['pwd'] != 'admin':
            error = 'Invalid user or password, Please try again.'
        else:
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

if __name__ == "__main__":
    """
    MAIN Flask App"""
    app.run(host=host, port=port, debug=True)
