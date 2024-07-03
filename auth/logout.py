#!/usr/bin/python3

from flask import Blueprint, redirect, url_for, flash, session, jsonify
from checker_handler import handle_checkout

logout = Blueprint('logout', __name__, static_folder='../static')


@logout.route('/logout/', methods=['GET'], strict_slashes=False)
def logout_usr():
    """
    Logout the user and clear session data.
    Redirect to login page.
    """
    if 'employee_id' in session:
        employee_id = session['employee_id']
        handle_checkout(employee_id)
        # session.pop('last_checkin', None)
        del session['employee_id']
        del session['employee_name']

    # session.clear()
    flash("You have been logged out.", 'info')
    return jsonify({"message": "logout successful"}), 200
