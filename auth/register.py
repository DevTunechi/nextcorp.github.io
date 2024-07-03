#!/usr/bin/python

from flask import Blueprint, render_template, redirect, url_for, flash, request
import requests


# register = Blueprint('register', __name__, template_folder='templates', static_folder='static')
register = Blueprint('register', __name__, template_folder='templates', static_folder='../static')
api_url = 'http://localhost:5000/api/corps'


def check_existing_corp_name(name):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            corps_data = response.json()
            return any(corp['name'] == name for corp in corps_data)
        else:
            flash("Error fetching existing corporations data from API")
            return False
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}")
        return False

def check_existing_corp_email(email):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            corps_data = response.json()
            return any(corp['email'] == email for corp in corps_data)
        else:
            flash("Error fetching existing corporations data from API")
            return False
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}")
        return False

@register.route('/register/', methods=['GET', 'POST'], strict_slashes=False)
def register_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not name or not email or not password:
            flash("All fields are required!")
            return redirect(url_for('register.register_page'))

        if password != confirm_password:
            flash("Passwords do not match!")
            return redirect(url_for('register.register_page'))

        if check_existing_corp_name(name):
            flash("Name '{}' already exists.".format(name))
            return redirect(url_for('register.register_page'))

        if check_existing_corp_email(email):
            flash("Email '{}' already exists.".format(email))
            return redirect(url_for('register.register_page'))

        if register_corp(name, email, password):
            flash("Registration successful!")
            return redirect(url_for('login.login_page'))
        else:
            flash("Error during registration")
            return redirect(url_for('register.register_page'))

    return render_template('register.html')

def register_corp(name, email, password):
    corp_data = {
        "name": name,
        "email": email,
        "passwd": password
    }

    try:
        response = requests.post(api_url, json=corp_data)
        if response.status_code == 201:
            return True
        elif response.status_code == 400:
            err_msg = response.json().get('error', 'Unknown error occurred')
            if "name" in err_msg:
                flash("Name '{}' already exists.".format(name))
            elif "email" in err_msg:
                flash("Email '{}' already exists.".format(email))
            else:
                flash(err_msg)
            return False
        else:
            flash("Error during registration")
            return False
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}")
        return False
