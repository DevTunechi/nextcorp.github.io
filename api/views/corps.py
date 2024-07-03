#!/usr/bin/python3
""" Corps-API-views """
from api.views import app_views
from flask import jsonify, request, abort
from sqlalchemy.exc import IntegrityError
from models import storage
from models.corp import Corp
import json
from uuid import uuid4

CORP_PATH = '/corps'


@app_views.route(CORP_PATH, methods=['GET'], strict_slashes=False)
def retrieve_corps():
    """ Gets list of all Corp objs """
    corp_recs = storage.all(Corp).values()
    return (json.dumps([crp.to_dict() for crp in corp_recs], indent=3) + '\n')


@app_views.route(CORP_PATH + '/<corp_id>', methods=['GET'], strict_slashes=False)
def retrieve_one_corp(corp_id):
    """ Gets a single corp obj based on id """
    print("<Line used for debugging:>\nCorp ID: ", corp_id)
    return (json.dumps(storage.get(Corp, corp_id).to_dict(), indent=3)
            + '\n' if storage.get(Corp, corp_id) else abort(404))


@app_views.route(CORP_PATH, methods=['POST'], strict_slashes=False)
def insert_corp():
    """ Creates a new Corp """
    dt = request.get_json() or abort(400, "Not a JSON")
    name = dt.get('name')
    email = dt.get('email')
    passwd = dt.get('passwd')

    if not name:
        return jsonify({"Error": "Name is missing"}), 400
    if not email:
        return jsonify({"Error": "Email is missing"}), 400
    if not passwd:
        return jsonify({"Error": "Password is missing"}), 400

    dt['id'] = str(uuid4())

    try:
        new_corp = Corp(**dt)
        storage.new(new_corp)
        storage.save()
    except IntegrityError:
        storage.rollback()
        abort(400, "Duplicate entry")
    except Exception as e:
        print("Exception: ", e)
        storage.rollback()
        # storage._DBStorage__session.rollback()
        abort(500, "Failed to create Corp due to database constraint violation")
    return (json.dumps(new_corp.to_dict()) + '\n', 201)


@app_views.route(CORP_PATH + '/<corp_id>', methods=['PUT'], strict_slashes=False)
def update_corp(corp_id):
    """ Updates a single Corp obj based on its id """
    corp_obj = storage.get(Corp, corp_id) or abort(404)
    dt = request.get_json() or abort(400, "Not a JSON")
    [setattr(corp_obj, k, val) for k, val in dt.items()
        if k not in ['id', 'created_at', 'updated_at']]

    storage.save()
    return (json.dumps(corp_obj.to_dict(), indent=3) + '\n', 200)


@app_views.route(CORP_PATH + '/<corp_id>', methods=['DELETE'], strict_slashes=False)
def del_corp(corp_id):
    """ Deletes a single Corp obj based on its id """
    corp_obj = storage.get(Corp, corp_id) or abort(404)
    try:
        storage.delete(corp_obj)
        storage.save()
        return (jsonify({}), 200)
    except Exception as e:
        return (jsonify({"Error": str(e)}), 500)
