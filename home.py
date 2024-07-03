#!/usr/bin/python3

from flask import Blueprint, render_template, session, redirect, url_for, flash
from employee_profile import get_employee_name
from checker_handler import API_URL


home = Blueprint('home', __name__, template_folder='templates', static_folder='static')


def render_home_page(last_checkin=None):
    """
        Renders the home page
        Checks & saves the employee name to session
        Displays if saved/found
        Check if last_checkin is valid
    """
    if 'employee_id' not in session:
        flash("You need to log in first.")
        return redirect(url_for('employee_login.login_page'))

    employee_id = session['employee_id']
    employee_name = session.get('employee_name')  

    if not employee_name:  
        employee_name = get_employee_name(employee_id) 
        if employee_name:
            session['employee_name'] = employee_name 
        else:
            flash("Failed to retrieve employee data.")
            return redirect(url_for('employee_login.login_page'))


    print(f"[Home Page] Employee ID in session: {employee_id}")
    print(f"[Home Page] Employee Name in session: {employee_name}")
    print(f"[Home Page] Full session: {session.items()}")
 
    if last_checkin is not None and 'checkin' not in last_checkin:
        last_checkin = None


    return render_template('home.html', employee_name=employee_name, employee_id=employee_id, last_checkin=last_checkin)
