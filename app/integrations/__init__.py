from flask import Blueprint
from flask_restful import Api


integrations_bp = Blueprint("integrations", __name__)
integrations_api = Api(integrations_bp)

from . import __routes__