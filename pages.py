#!/usr/bin/python3

from flask import Blueprint, render_template

view = Blueprint('view', __name__, template_folder='templates')

@view.route('/', strict_slashes=False)
@view.route('/home/', strict_slashes=False)
def home_page():
    return render_template('home.html')
