#!/usr/bin/python3
""" States file """
from api.v1.views import app_views
from flask import abort, jsonify
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_states(state_id=None):
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
