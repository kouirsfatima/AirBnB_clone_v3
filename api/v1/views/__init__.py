#!/usr/bin/pyhton3
"""create app_views instance"""
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
# from api.v1.views.states import *