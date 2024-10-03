from flask import Blueprint
from flask_restful import Api


loans_bp = Blueprint("loans", __name__)
loans_api = Api(loans_bp)

from . import __routes__