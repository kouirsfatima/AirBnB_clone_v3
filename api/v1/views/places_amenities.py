#!/usr/bin/python3
""" Place_amenities file """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.place import Place
from models.amenity import Amenity

from models import storage, storage_t


@app_views.route(
    '/places/<place_id>/amenities', methods=['GET'], strict_slashes=False
)
def get_place_amenity(place_id):
    """Retrieves the list of all place_amenities"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenities_list = []
    if storage_t == "db":
        for amenity in place.amenities:
            amenities_list.append(amenity.to_dict())
    else:
        for amenity_id in place.amenity_ids:
            amenity = storage.get(Amenity, amenity_id)
            amenities_list.append(amenity.to_dict())

    return jsonify(amenities_list)

@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>", strict_slashes=False, methods=["DELETE"]
)
def delete_place_amenity(place_id, amenity_id):
    """ Deletes a Place_amenity Object """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity_id)

    storage.delete(amenity)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def post_place_amenity(place_id, amenity_id):
    """ link a Amenity object to a Place """

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if storage_t == "db":
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
