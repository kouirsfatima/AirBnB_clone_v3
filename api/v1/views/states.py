#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, request, jsonify


@app_views.route("/states", strict_slashes=False, methods=["GET"])
@app_views.route("/states/<state_id>", strict_slashes=False, methods=["GET"])
def states(state_id=None):
    """show states and states with id"""
    states_list = []
    if state_id is None:
        all_objs = storage.all(State).values()
        for v in all_objs:
            states_list.append(v.to_dict())
        return jsonify(states_list)
    else:
        result = storage.get(State, state_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/states/<state_id>", strict_slashes=False,
                 methods=["DELETE"])
def states_delete(state_id):
    """delete method"""
    obj = storage.get(State, state_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a State Object"""
    if not request.get_json():
        return make_response("Not a JSON", 400)
    if 'name' not in request.get_json():
        return make_response("Missing name", 400)

    data = request.get_json()
    new_state = State(name=data["name"])
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def Update_state(state_id):
    """update a State Object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    keys = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in keys:
            if hasattr(state, key):
                setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
