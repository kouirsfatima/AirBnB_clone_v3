#!/usr/bin/python3
""" Cities file """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.review import Review
from models.user import User
from models.place import Place
from models import storage


@app_views.route(
   '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False
)
@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_reviwes(place_id=None, review_id=None):
    """Retrieves the list of all reviews"""
    if review_id:
        review = storage.get(Review, review_id)
        if not review:
            abort(404)
        else:
            return jsonify(review.to_dict())

    if place_id:
        place = storage.get(Place, place_id)
        if not place:
            abort(404)
        reviews = storage.all(Review).values()
        reviews_list = []

        for review in reviews:
            if review.place_id == place_id:
                reviews_list.append(review.to_dict())

        return jsonify(reviews_list)

@app_views.route(
    "/reviews/<review_id>", strict_slashes=False, methods=["DELETE"]
)
def delete_review(review_id):
    """ Deletes a Review Object """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response(jsonify({}), 200)

@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False,
)
def create_review(place_id):
    """Create a reviews Object"""
    place = storage.get(Place, place_id)
    if not place:
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

    if 'text' not in data:
        return make_response("Missing text", 400)

    text = data.get("text")

    new_review = Review(text=text, user_id=user_id, place_id=place_id)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """update a reviews Object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.get_json():
        return make_response("Not a JSON", 400)

    data = request.get_json()
    keys = ["id", "created_at", "updated_at", "user_id", "place_id"]

    for key, value in data.items():
        if key not in keys:
            if hasattr(review, key):
                setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
