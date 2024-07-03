#!/usr/bin/python3

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
import requests
from checker_handler import API_URL, handle_checkin


employee_login = Blueprint('employee_login', __name__, template_folder='templates', static_folder='../static')
api_url = 'http://localhost:5000/api/employees'

@employee_login.route('/employee_login/', methods=['GET', 'POST'], strict_slashes=False)
def login_page():
    """
        Check in employee
        Fetch check-in/out data after check-in and store in session
        Retrieve last checkin if exists
        Doesn't render the last check-in if there is a checkout time
    """
    if request.method == 'POST':
        employee_id = request.form.get('employee_id')
        password = request.form.get('password')

        if authenticate_employee(employee_id, password):
            flash("Login successful!")
            session['employee_id'] = employee_id
            employee_data = get_employee_data(employee_id)
            if employee_data:
                session['employee_name'] = employee_data['name']
                print(f"[Login Page] Set Employee Name in session: {session['employee_name']}")
                print(f"[Login Page 1] Full session after setting employee name: {session.items()}")

                handle_checkin(employee_id)
                response = requests.get(f"{API_URL}/employees/{employee_id}/last_checkin")
                if response.status_code == 200:
                    last_checkin = response.json()
                    if last_checkin and last_checkin.get("checkout") is None:
                        session["last_checkin"] = last_checkin  
                    
                    print(f"[Login Page] Updated session with last_checkin: {session.items()}")
                    print(f"[Login Page 1] last_checkin from GET: {last_checkin}")
                else:
                    flash("Failed to retrieve check-in data.")
                    return redirect(url_for('employee_login.login_page'))

            else:
                flash("Failed to retrieve employee data.")
                return redirect(url_for('employee_login.login_page'))

            return redirect(url_for('home_page'))
        else:
            flash("Invalid Credentials.")
            return redirect(url_for('employee_login.login_page'))
   
    last_checkin = session.get('last_checkin')
    print(f"[Login Page 2] last_checkin from GET: {last_checkin}")

    employee_id = session.get('employee_id')
    print("[Login Page 3] employee_id from GET: ".format(employee_id))

    if last_checkin is not None and 'checkout' in last_checkin:
        last_checkin = None
    
    return render_template('employee_login.html', last_checkin=last_checkin, employee_id=employee_id)

def authenticate_employee(employee_id, password):
    try:
        response = requests.get(f"{api_url}/{employee_id}")
        if response.status_code == 200:
            employee_data = response.json()
            print("[Login Page] Employee data retrieved: ", employee_data)
            print(f"[Login Page] Input password: {password}, Stored password: {employee_data['passwd']}")

            if employee_data['passwd'] == password:
                print("[Login Page] Password match successful!")
                return True
            else:
                print("[Login Page] Password does not match.")
        else:
            print("[Login Page] Failed to retrieve employee data.")
        return False
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}")
        return False


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
