#!/usr/bin/python3
""" Flask app """
from flask import Flask, jsonify, make_response
from os import environ
from models import storage
from api.v1.views import app_views
from flask_cors import CORS


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

app.register_blueprint(app_views)
app.url_map.strict_slashes = False


@app.teardown_appcontext
def close_db(error):
    """closes the storage on teardown"""
    storage.close()


@app.errorhandler(404)
def not_found(error):
    """errorhandler"""
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == "__main__":

    host = environ.get('HBNB_API_HOST', '0.0.0.0')
    port = environ.get('HBNB_API_PORT', 5000)

    app.run(host=host, port=int(port), threaded=True)
