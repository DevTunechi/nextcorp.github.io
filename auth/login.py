#!/usr/bin/python3

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
import requests

login = Blueprint('login', __name__, template_folder='templates', static_folder='../static')
api_url = 'http://localhost:5000/api/corps'


@login.route('/login/', methods=['GET', 'POST'], strict_slashes=False)
def login_page():
    """
       Retrieve form data
       Check if any field is missing
       Authenticate the corporation using corp_id and password
       Redirect to a dashboard or home page after successful login
       Returns the login page template
    """
    if request.method == 'POST':
        corp_id = request.form.get('corp_id')
        password = request.form.get('password')

        if not corp_id or not password:
            flash("All fields are required!")
            return redirect(url_for('login.login_page'))

        if authenticate_corp(corp_id, password):
            flash("Login successful!")
            session['corp_id'] = corp_id
            return redirect(url_for('dashboard.dashboard_page'))
        else:
            flash("Invalid Credentials.")
            return redirect(url_for('login.login_page'))

    return render_template('login.html')


def authenticate_corp(corp_id, password):
    """
        Function to authenticate the corporation
        Check if the password matches
    """
    try:
        response = requests.get(f"{api_url}/{corp_id}")
        if response.status_code == 200:
            corp_data = response.json()

            if corp_data['passwd'] == password:
                return True
        return False
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}")
        return False
