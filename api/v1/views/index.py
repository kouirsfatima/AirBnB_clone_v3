#!/usr/bin/python3
""" Index file """
from api.v1.views import app_views
from flask import jsonify



@app_views.route('/status')
def status():
    """return status ok"""
    return jsonify({"status": "OK"})






# from models.amenity import Amenity
# from models.city import City
# from models.place import Place
# from models.review import Review
# from models.state import State
# from models.user import User
# from models import storage

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
