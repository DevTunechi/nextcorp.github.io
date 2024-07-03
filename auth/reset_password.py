#!/usr/bin/python3

from flask import Blueprint, render_template, redirect, url_for, flash, request
import requests

reset = Blueprint('reset_password', __name__, template_folder='templates', static_folder='../static')
api_url = 'http://localhost:5000/api/corps'


@reset.route('/reset', methods=['GET', 'POST'], strict_slashes=False)
def reset_password_page():
    """
    Display form to reset password and handle password reset.
    """
    corp_id = request.args.get('corp_id')

    if not corp_id:
        flash('No corp_id provided.', 'danger')
        return redirect(url_for('login.login_page'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('reset_password.reset_password_page', corp_id=corp_id))
        else:
            if reset_password_for_corp(corp_id, new_password):
                flash('Password reset successfully!', 'success')
                return redirect(url_for('login.login_page'))
            else:
                flash('Failed to reset password. Please try again later.', 'danger')

    return render_template('reset_password.html', corp_id=corp_id)


def reset_password_for_corp(corp_id, new_password):
    """
    Function to reset password for a corporation.
    """
    try:
        response = requests.put(f"{api_url}/{corp_id}", json={"passwd": new_password})
        if response.status_code == 200:
            return True
        else:
            flash(f"Error resetting password: {response.text}", 'danger')
            return False
    except requests.exceptions.RequestException as e:
        flash(f"Error: {str(e)}", 'danger')
        return False
