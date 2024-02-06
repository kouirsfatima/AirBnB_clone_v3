#!/usr/bin/python3
""" States file """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states(state_id=None):
    """Retrieves the list of all State"""
    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        else:
            return jsonify(state.to_dict())

    else:
        states = storage.all(State).values()
        states_list = []

        for state in states:
            states_list.append(state.to_dict())

        return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a State Object """
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return make_response(jsonify, ({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Create a State Object"""
    if not request.get_json():
        return make_response("Not a JSON", 400)
    if 'name' not in request.get_json():
        return make_response("Missing name", 400)

    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["put"], strict_slashes=False)
def Update_state():
    """update a State Object"""
    if not request.get_json():
        return make_response("Not a JSON", 400)
    if 'name' not in request.get_json():
        return make_response("Missing name", 400)
    data = request.get_json()
    keys = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in keys:
            object.name = data.get("name", object.name)
    storage.save(data)
    return make_response(jsonify(data), 200)
