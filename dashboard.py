#!/usr/bin/python3

from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
import requests, json

dash = Blueprint('dashboard', __name__, template_folder='templates', static_folder='static')
api_url = 'http://localhost:5000/api'

@dash.route('/dashboard', methods=['GET'], strict_slashes=False)
def dashboard_page():
    corp_id = session.get('corp_id')

    if not corp_id:
        flash("You can't access this page you need to login first.")
        return redirect(url_for('login.login_page'))

    try:
        employees_response = requests.get("{}/corps/{}/employees".format(api_url, corp_id))
        if employees_response.status_code == 200:
            employees = employees_response.json()
            return render_template('dashboard.html', employees=employees, update_employee=None, action="list")
        else:
            flash("Error fetching employees")
            return render_template('dashboard.html', employees=[], update_employee=None, action="list")
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}")
        return render_template('dashboard.html', employees=[], update_employee=None, action="list")


@dash.route('/dashboard/add', methods=['GET', 'POST'], strict_slashes=False)
def add_employee():
    corp_id = session.get('corp_id')

    if request.method == 'GET':
        return render_template('dashboard.html', employees=[], update_employee=None, action="add")

    if not corp_id:
        flash("You can't access this page you need to login first.") 
        return redirect(url_for('login.login_page'))

    is_hr = request.form.get('is_hr', 'false').lower() == 'true'
    corp_position = request.form.get('corp_position')
    if is_hr:
        corp_position = "Human Resources"

    data = {
        "name": request.form.get('name'),
        "email": request.form.get('email'),
        "passwd": request.form.get('passwd'),
        "birth_date": request.form.get('birth_date'),
        "card_id_number": request.form.get('card_id_number'),
        "phone_number": request.form.get('phone_number'),
        "is_hr": is_hr,
        "joined_date": request.form.get('joined_date'),
        "expiry_date": request.form.get('expiry_date'),
        "corp_position": corp_position
    }

    try:
        response = requests.post(f"{api_url}/corps/{corp_id}/employees", json=data)
        if response.status_code == 201:
            flash("Employee added successfully!", 'success')
        else:
            try:
                response_data = response.json()
                err_msg = response_data.get('error', 'Unknown error')
            except json.decoder.JSONDecodeError:
                err_msg = "Unexpected response: {}".format(response.text)
            if response.status_code == 400 and 'Duplicate entry' in err_msg:
                err_msg = "Error adding employee: Duplicate entry."
            flash(err_msg, 'danger')
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}", 'danger')
    
    return redirect(url_for('dashboard.dashboard_page'))


@dash.route('/dashboard/update/<employee_id>', methods=['GET', 'POST'], strict_slashes=False)
def update_employee(employee_id):
    corp_id = session.get('corp_id')

    if not corp_id:
        flash("You can't access this page you need to login first.")
        return redirect(url_for('login.login_page'))

    if request.method == 'GET':
        try:
            employee_response = requests.get(f"{api_url}/employees/{employee_id}")
            if employee_response.status_code == 200:
                employee = employee_response.json()
                return render_template('dashboard.html', employees=[], update_employee=employee, action="update")
            else:
                flash("Error fetching employee data")
                return redirect(url_for('dashboard.dashboard_page'))
        except requests.exceptions.RequestException as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for('dashboard.dashboard_page'))

    is_hr = request.form.get('is_hr') == 'on'
    corp_position = request.form.get('corp_position')
    if is_hr:
        corp_position = "Human Resources"

    expiry_date = request.form.get('expiry_date')
    if not expiry_date:
        expiry_date = None

    updated_data = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "passwd": request.form.get('passwd'),
            "birth_date": request.form.get('birth_date'),
            "card_id_number": request.form.get('card_id_number'),
            "phone_number": request.form.get('phone_number'),
            "is_hr": is_hr,
            "joined_date": request.form.get('joined_date'),
            "expiry_date": expiry_date,
            "corp_position": corp_position
    }

    update_response = requests.put(f"{api_url}/employees/{employee_id}", json=updated_data)
    if update_response.status_code == 200:
        flash("Employee updated successfully!")
    else:
        flash("Error updating employee, Data already exists!")
    
    return redirect(url_for('dashboard.dashboard_page'))

@dash.route('/dashboard/delete/<employee_id>', methods=['DELETE'], strict_slashes=False)
def delete_employee(employee_id):
    corp_id = session.get('corp_id')
    
    if not corp_id:    
        return jsonify({"error": "You can't access this page you need to login first."}), 403

    try:
        response = requests.delete("{}/employees/{}".format(api_url, employee_id))
        if response.status_code == 200:
            return jsonify({"message": "Employee deleted successfully!"}), 200
        else:
            return jsonify({"error": response.json().get('error', 'Unknown error')}), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
