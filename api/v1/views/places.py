#!/usr/bin/python3
""" Cities file """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.city import City
from models.state import State

from models import storage


@app_views.route(
    '/states/<state_id>/cities', methods=['GET'], strict_slashes=False
)
@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id=None, state_id=None):
    """Retrieves the list of all Cites"""
    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        else:
            return jsonify(city.to_dict())

    if state_id:
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        cities = storage.all(City).values()
        cities_list = []

        for city in cities:
            if city.state_id == state_id:
                cities_list.append(city.to_dict())

        return jsonify(cities_list)


@app_views.route(
    "/cities/<city_id>", strict_slashes=False, methods=["DELETE"]
)
def delete_city(city_id):
    """ Deletes a City Object """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """Create a City Object"""
    if not request.get_json():
        return make_response("Not a JSON", 400)
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if 'name' not in request.get_json():
        return make_response("Missing name", 400)

    data = request.get_json()
    new_state = City(name=data.get('name'), state_id=state_id)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def Update_city(city_id):
    """update a City Object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        return make_response("Not a JSON", 400)
    data = request.get_json()
    keys = ["id", "created_at", "updated_at", "state_id"]

    for key, value in data.items():
        if key not in keys:
            if hasattr(city, key):
                setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
