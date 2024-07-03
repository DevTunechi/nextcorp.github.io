#!/usr/bin/python3
""" Employees-API-views """
from api.views import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from models import storage
from models.corp import Corp
from models.employee import Employee
import json
from uuid import uuid4
from datetime import datetime

CORP_PATH = '/corps'
EMP_PATH = '/employees'


@app_views.route(CORP_PATH + '/<corp_id>' + EMP_PATH, methods=['GET'],
                 strict_slashes=False)
def retrieve_employees(corp_id):
    """ Retrieves list of all Employee objs of a Corp """
    corp_obj = storage.get(Corp, corp_id) or abort(404)
    return (json.dumps([crp.to_dict() for crp in corp_obj.employees],
            indent=3) + '\n', 200)


@app_views.route(EMP_PATH + '/<employee_id>', methods=['GET'], strict_slashes=False)
def retrieve_one_employee(employee_id):
    """ Gets a single Employee based on its id """
    print("<Line used for debugging:>\nEmployee ID: ", employee_id)
    return (json.dumps(storage.get(Employee, employee_id).to_dict(), indent=3)
            + '\n' if storage.get(Employee, employee_id) else abort(404))



@app_views.route(CORP_PATH + '/<corp_id>' + EMP_PATH,
                 methods=['POST'], strict_slashes=False)
def insert_employee(corp_id):
    """ Inserts a new Employee """
    corp_obj = storage.get(Corp, corp_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")

    print("Received data: ", dt)

    name = dt.get('name') or abort(400, "Name is missing")
    email = dt.get('email') or abort(400, "Email is missing")
    passwd = dt.get('passwd') or abort(400, "Password is missing")
    birth_date_str = dt.get('birth_date') or abort(400, "Birthdate is missing")
    card_id_number = dt.get('card_id_number') or abort(400, "Card-Id number is missing")
    phone_number = dt.get('phone_number') or abort(400, "Phone number is missing")

    try:
        birth_date = datetime.fromisoformat(birth_date_str)
    except ValueError:
        abort(400, "Invalid birth_date format. Should be YYYY-MM-DDTHH:MM:SS")

    is_hr = dt.get('is_hr', False)
    joined_date = dt.get('joined_date', datetime.utcnow())
    expiry_date_str = dt.get('expiry_date', None)

    expiry_date = None
    if expiry_date_str:
        try:
            expiry_date = datetime.fromisoformat(expiry_date_str)
        except ValueError:
            abort(400, "Invalid expiry_date format. Should be YYYY-MM-DDTHH:MM:SS")

    corp_position = dt.get('corp_position', "None")
    
    dt.update({'corp_id': corp_id,
               'name': name,
               'email': email,
               'passwd': passwd,
               'birth_date': birth_date,
               'card_id_number': card_id_number,
               'phone_number': phone_number,
               'is_hr': is_hr,
               'joined_date': joined_date,
               'expiry_date': expiry_date,
               'corp_position': corp_position})

    try:
        new_employee = Employee(**dt)
        print("Created new_employee: ", new_employee)
        storage.new(new_employee)
        storage.save()
    except IntegrityError as ie:
        print("IntegrityError: ", ie)
        storage.rollback()
        abort(400, "Duplicate entry")
    except Exception as e:
        print("Exception: ", e)
        storage.rollback()
        abort(500, "Failed to create Employee due to database constraint violation")
    return (json.dumps(new_employee.to_dict()) + '\n', 201)


@app_views.route(EMP_PATH + '/<employee_id>', methods=['PUT'], strict_slashes=False)
def updates_employee(employee_id):
    """ updates an Employee obj """
    employee_obj = storage.get(Employee, employee_id) or abort(404, "Employee not found")
    dt = request.get_json() or abort(400, "NOT a JSON")
    ignore_keys = {'id', 'corp_id', 'created_at', 'updated_at'}
    [setattr(employee_obj, k, val) for k, val in dt.items()
        if k not in ignore_keys]
    storage.save()
    return (json.dumps(employee_obj.to_dict(), indent=2) + '\n', 200)
    

@app_views.route(EMP_PATH + '/<employee_id>', methods=['DELETE'], strict_slashes=False)
def del_employee(employee_id):
    """ Deletes a single employee obj """
    employee_obj = storage.get(Employee, employee_id) or abort(404, "Employee not found")
    try:
        storage.delete(employee_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"Error": str(e)}), 500)
