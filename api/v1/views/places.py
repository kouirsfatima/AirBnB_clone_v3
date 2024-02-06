#!/usr/bin/python3
""" Cities file """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.city import City
from models.user import User

from models import storage


@app_views.route(
    '/cities/<city_id>/places', methods=['GET'], strict_slashes=False
)
@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_places(place_id=None, city_id=None):
    """Retrieves the list of all places"""
    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        else:
            return jsonify(place.to_dict())

    if city_id:
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        places = storage.all(Place).values()
        places_list = []

        for place in places:
            if place.city_id == city_id:
                places_list.append(place.to_dict())

        return jsonify(places_list)


@app_views.route(
    "/places/<place_id>", strict_slashes=False, methods=["DELETE"]
)
def delete_place(place_id):
    """ Deletes a Place Object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """Create a Place Object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        return make_response("Not a JSON", 400)

    data = request.get_json()

    if 'user_id' not in data:
        return make_response("Missing user_id", 400)

    user_id = data.get("user_id")

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    if 'name' not in data:
        return make_response("Missing name", 400)

    name = data.get("name")

    new_place = Place(name=name, user_id=user_id, city_id=city_id)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route("places/<place_id>", methods=["PUT"], strict_slashes=False)
def Update_place(place_id):
    """update a Place Object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response("Not a JSON", 400)
    data = request.get_json()
    keys = ["id", "created_at", "updated_at", "user_id", "user_id"]

    for key, value in data.items():
        if key not in keys:
            if hasattr(place, key):
                setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
