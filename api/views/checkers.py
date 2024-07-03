#!/usr/bin/python3
""" Employees-API-views """
from api.views import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from models import storage
from models.employee import Employee
from models.checker import CheckInOut
import json
from uuid import uuid4
from datetime import datetime


EMP_PATH = '/employees'
CIO_PATH = '/checkers'


@app_views.route(EMP_PATH + '/<employee_id>' + CIO_PATH, methods=['GET'],
                 strict_slashes=False)
def retrieve_checkers(employee_id):
    """ Retrieves list of Checker objs of an Employee """
    employee_obj = storage.get(Employee, employee_id) or abort(404)
    return (json.dumps([emp.to_dict() for emp in employee_obj.checkinsouts],
            indent=3) + '\n', 200)


@app_views.route(CIO_PATH + '/<cio_id>', methods=['GET'], strict_slashes=False)
def retrieve_one_checker(cio_id):
    """ Gets a single Checker based on its id """
    print("<Line used for debugging:>\nChecker ID: ", cio_id)
    return (json.dumps(storage.get(CheckInOut, cio_id).to_dict(), indent=3)
            + '\n' if storage.get(CheckInOut, cio_id) else abort(404))


@app_views.route(EMP_PATH + '/<employee_id>' + CIO_PATH,
                 methods=['POST'], strict_slashes=False)
def insert_checker(employee_id):
    """ Creates a checker obj based on an employee id """
    employee_obj = storage.get(Employee, employee_id) or abort(404, "Employee not found")
    dt = request.get_json() or abort(400, "NOT a JSON")

    print("Received data: ", dt)

    checkin_str = dt.get('checkin') or abort(400, "Check-in time is missing")
    try:
        checkin = datetime.fromisoformat(checkin_str)
    except ValueError:
        abort(400, "Invalid check-in format. Should be YYYY-MM-DDTHH:MM:SS")

    checkout_str = dt.get('checkout', None)
    checkout = None
    if checkout_str:
        try:
            checkout = datetime.fromisoformat(checkout_str)
        except ValueError:
            abort(400, "Invalid check-out format. Should be YYYY-MM-DDTHH:MM:SS")

    dt.update({'user_id': employee_id,
               'checkin': checkin,
               'checkout': checkout})
    try:
        new_checkinout = CheckInOut(**dt)
        print("Checkers created: ", new_checkinout)
        storage.new(new_checkinout)
        storage.save()
    except IntegrityError as ie:
        print("IntegrityError: ", ie)
        storage.rollback()
        abort(400, "Duplicate entry")
    except Exception as e:
        print("Exception: ", e)
        storage.rollback()
        abort(500, "Failed to create CheckInOut due to database constraint violation")
    return (json.dumps(new_checkinout.to_dict()) + '\n', 201)

@app_views.route(EMP_PATH + '/<employee_id>/last_checkin', methods=['GET'], strict_slashes=False)
def get_last_checkin(employee_id):
    """Retrieves the latest active check-in/out record for an employee."""
    employee_obj = storage.get(Employee, employee_id)
    if not employee_obj:
        abort(404)
        
    checkers = sorted(employee_obj.checkinsouts, key=lambda x: x.checkin, reverse=True)
    last_checkin = next((check for check in checkers if not check.checkout), None)

    return jsonify(last_checkin.to_dict() if last_checkin else None), 200


@app_views.route(CIO_PATH + '/<cio_id>', methods=['PUT'], strict_slashes=False)
def updates_checker(cio_id):
    """ updates a Checker obj """
    checker_obj = storage.get(CheckInOut, cio_id) or abort(404, "CheckInOut not found")
    dt = request.get_json() or abort(400, "NOT a JSON")
    ignore_keys = {'id', 'employee_id', 'created_at'}

    if 'checkout' in dt and dt['checkout'] is not None:
        try:
            checkout_time = datetime.fromisoformat(dt['checkout'])
            checker_obj.checkout = checkout_time
            storage.save()
            return jsonify(checker_obj.to_dict()), 200
        except ValueError:
            abort(400, "Invalid checkout format. Should be YYYY-MM-DDTHH:MM:SS")
    else:
        abort(400, "Only checkout updates are allowed.")
    

@app_views.route(CIO_PATH + '/<cio_id>', methods=['DELETE'], strict_slashes=False)
def del_checker(cio_id):
    """ Deletes a single checker obj """
    pass
