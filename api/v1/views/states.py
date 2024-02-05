#!/usr/bin/python3
""" States file """
from api.v1.views import app_views
from flask import abort, jsonify, make_response
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

    return make_response(jsonify ({}), 200)
