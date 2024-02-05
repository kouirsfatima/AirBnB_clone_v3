#!/usr/bin/python3
""" Index file """

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.amenity import Amenity


@app_views.route('/status', strict_slashes=False, methods=["GET"])
def status():
    """return status ok"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False, methods=["GET"])
def get_stats():
    """retrieves the number of each objects by type"""
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        })


# app = Flask(__name__)
# app.url_map.strict_slashes = False

# @app_views.route('/stats', methods=['GET'])
# def number_of_object():
#     classes = {"Amenity": Amenity,"City": City,
#              "Place": Place, "Review": Review, "State": State, "User": User}
#     states = {}
#     for cl_name, cl_type in classes.items():
#         count = storage.count(cl_type)
#         states[cl_name] = count
#     return jsonify(states)
