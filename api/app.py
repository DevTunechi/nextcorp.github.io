#!/usr/bin/env python3

from flask import Flask, jsonify, session, url_for, redirect, flash
from flask_cors import CORS
import requests
from flask_session import Session
from models import storage
from api.views import app_views
import os
from os import getenv
from pages import view
from auth.register import register
from auth.login import login
from auth.logout import logout
from auth.reset_password import reset
from dashboard import dash
from auth.employee_login import employee_login
from employee_profile import profile
from home import home, render_home_page
from checker_handler import API_URL


app = Flask(__name__, static_folder='../static', template_folder='../templates')
CORS(app)
app.config['SECRET_KEY'] = getenv('SECRET_KEY', os.urandom(24))
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = './flask_session/'
app.config['SESSION_PERMANENT'] = False
Session(app)


app.register_blueprint(app_views)
app.register_blueprint(view)
app.register_blueprint(register, url_prefix='/corp_auth')
app.register_blueprint(login, url_prefix='/corp_auth')
app.register_blueprint(reset, url_prefix='/corp_auth')
app.register_blueprint(dash, url_prefix='/admin')
app.register_blueprint(logout, url_prefix='/auth')
app.register_blueprint(employee_login, url_prefix='/auth')
app.register_blueprint(profile, url_prefix='/profile')
app.register_blueprint(home)


@app.route('/home', defaults={'trailing_slash': False}, strict_slashes=False)
@app.route('/', defaults={'trailing_slash': False}, strict_slashes=False)
def home_page(trailing_slash):
    """ Removes trailing slash if present and renders home_page """
    if trailing_slash:
        return redirect(url_for('home_page'))

    last_checkin = session.get('last_checkin')
    return render_home_page(last_checkin=last_checkin)


@app.errorhandler(404)
def trigger_error(err):
    """ Triggers a 404 error """
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def teardown_db(exception):
    """ Close storage on teardown """
    storage.close()


if __name__ == '__main__':
    """ Runs flask app on a specified adr and port """
    host = getenv('NC_API_HOST', '0.0.0.0')
    port = int(getenv('NC_API_PORT', '5000'))
    app.run(host=host, port=port, threaded=True, debug=True)
