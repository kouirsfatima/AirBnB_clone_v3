#!/usr/bin/python3
""" Index file """
from api.v1.views import app_views
from flask import Flask, abort, jsonify, make_response, request
from models.state import State
from models import storage

app = Flask(__name__)
app.url_map.strict_slashes = False
@app_views.route('/states', methods=['GET'])
@app_views.route("/states/<state_id>", methods=["GET"])
def get_states(state_id):
    states = storage.all(State).values()
    states_list = []

    for state in states:
        states_list.append(state.to_dict())

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(states_list)
