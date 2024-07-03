#!/usr/bin/env python3

from api.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Returns API status """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def retrieve_stats():
    """ Retrieves class stats """
    cls_counts = {"corps": storage.count("Corp"),
                  "employees": storage.count("Employee"),
                  "checkinsouts": storage.count("CheckInOut")}
    return jsonify(cls_counts)
