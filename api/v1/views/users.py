#!/usr/bin/python3
""" Cities file """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_users(user_id=None):
    """Retrieves the list of all Users"""
    if user_id:
        user = storage.get(User, user_id)
        if not user:
            abort(404)
        else:
            return jsonify(user.to_dict())

    else:
        users = storage.all(User).values()
        users_list = []

        for user in users:
            users_list.append(user.to_dict())

        return jsonify(users_list)


@app_views.route(
    "/users/<user_id>", strict_slashes=False, methods=["DELETE"]
)
def delete_user(user_id):
    """ Deletes a User Object """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Create a User Object"""
    if not request.get_json():
        return make_response("Not a JSON", 400)
    if 'email' not in request.get_json():
        return make_response("Missing email", 400)
    if 'password' not in request.get_json():
        return make_response("Missing password", 400)

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    new_user = User(email=email, password=password)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def Update_user(user_id):
    """update a User Object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        return make_response("Not a JSON", 400)
    data = request.get_json()
    keys = ["id", "created_at", "updated_at", "email"]

    for key, value in data.items():
        if key not in keys:
            if hasattr(user, key):
                setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
