#!/usr/bin/python3

from flask import Blueprint, render_template, session, redirect, url_for, flash, request
import requests


profile = Blueprint('employee_profile', __name__, template_folder='templates', static_folder='static')
api_url = 'http://localhost:5000/api/employees'


@profile.route('/', methods=['GET', 'POST'], strict_slashes=False)
def profile_page():
    if 'employee_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('employee_login.login_page'))

    employee_id = session['employee_id']
    employee_data = get_employee_data(employee_id)

    if not employee_data:
        flash("Failed to retrieve employee data.")
        return redirect(url_for('employee_login.login_page'))

    employee_data['birth_date'] = employee_data.get('birth_date', '').split('T')[0] if employee_data.get('birth_date') else ''

    if request.method == 'POST':
        updated_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'passwd': request.form.get('passwd'),
            'birth_date': request.form.get('birth_date'),
            'card_id_number': request.form.get('card_id_number'),
            'phone_number': request.form.get('phone_number')
        }

        if update_employee_data(employee_id, updated_data):
            flash("Employee data updated successfully!")
            session['employee_name'] = updated_data['name']
            return redirect(url_for('employee_profile.profile_page'))
        else:
            flash("Failed to update employee data.")

    return render_template('employee_profile.html', employee_data=employee_data)


@profile.route('/view', methods=['GET'])
def view_profile():
    if 'employee_id' not in request.args:
        flash("Employee ID not provided.")
        return redirect(url_for('employee_profile.profile_page'))

    employee_id = request.args['employee_id']
    employee_data = get_employee_data(employee_id)

    if not employee_data:
        flash("Failed to retrieve employee data.")
        return redirect(url_for('employee_profile.profile_page'))

    employee_data['birth_date'] = employee_data.get('birth_date', '').split('T')[0] if employee_data.get('birth_date') else ''

    return render_template('employee_profile.html', employee_data=employee_data)


def get_employee_data(employee_id):
    try:
        response = requests.get(f"{api_url}/{employee_id}")
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}")
        return None


def update_employee_data(employee_id, updated_data):
    try:
        response = requests.put(f"{api_url}/{employee_id}", json=updated_data)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}")
        return False


def get_employee_name(employee_id):
    employee_data = get_employee_data(employee_id)
    print(f"Employee Data for {employee_id}: {employee_data}")
    if employee_data:
        return employee_data.get('name')
    return None
