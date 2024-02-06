#!/usr/bin/python3
""" States file """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route(
    "/amenities/<amenity_id>", methods=["GET"], strict_slashes=False
)
def get_amentiy(amenity_id=None):
    """Retrieves the list of all amenties"""
    if amenity_id:
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            abort(404)

        else:
            return jsonify(amenity.to_dict())

    else:
        amenities = storage.all(Amenity).values()
        amenity_list = []
        for amenity in amenities:
            amenity_list.append(amenity.to_dict())
        return jsonify(amenity_list)


@app_views.route(
    "/amenities/<amenity_id>", strict_slashes=False, methods=["DELETE"]
)
def delete_amenity(amenity_id):
    """ Deletes an Amenity Object """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Create a amenity Object"""
    if not request.get_json():
        return make_response("Not a JSON", 400)
    if 'name' not in request.get_json():
        return make_response("Missing name", 400)

    data = request.get_json()
    new_amenity = Amenity(name=data.get('name'))
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route(
    "/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False
)
def Update_Amenity(amenity_id):
    """update an Amenity Object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        return make_response("Not a JSON", 400)
    data = request.get_json()
    keys = ["id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in keys:
            if hasattr(amenity, key):
                setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
