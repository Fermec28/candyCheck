#!/usr/bin/python3
"""
Flask App that integrates with AirBnB static HTML Template
"""
from flask import Flask, render_template, url_for, request, redirect
from flask import make_response
from models import storage
import uuid


# flask setup
app = Flask(__name__)
app.url_map.strict_slashes = False
port = 5000
host = '0.0.0.0'

aut_data = {'email': '769@holbertonschool.com',
            'pwd': 'Angel1406*'}

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
        if request.form['email'] == aut_data['email'] and request.form['pwd'] == aut_data['pwd']:
            return redirect(url_for('home'))
        else:
            error = 'Invalid user or password, Please try again.'
    return render_template('login.html', error=error)


@app.route('/home', methods=['GET'])
def home():
    cookie = str(uuid.uuid4())
    resp = make_response(render_template('home.html', cache_id=uuid.uuid4()))
    """ Set cookie time expires in 1 hour"""
    resp.set_cookie("auth", cookie, max_age=60*60)
    return resp


if __name__ == "__main__":
    """
    MAIN Flask App"""
    app.run(host=host, port=port, debug=True)
