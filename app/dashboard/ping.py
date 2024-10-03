from flask import jsonify
from datetime import datetime
import platform
from flask_restful import Resource

from app.general import getUtcCurrentTime



def generate_deployment_details():
    # Automatically generate deployment details
    current_time = getUtcCurrentTime()  # Current time in UTC
    deployment_type = "Automated"  # This could be fetched or set dynamically

    deployment_details = {
        "deployed_on_time": True,  # You can add logic to determine this
        "deployment_date": current_time.strftime("%Y-%m-%d"),
        "deployment_time": current_time.strftime("%H:%M:%S UTC"),
        "deployment_type": deployment_type,
        "system": platform.system(),
        "release": platform.release(),
        "python_version": platform.python_version(),
        # Add other auto-generated details if necessary
    }

    return deployment_details


class Ping(Resource):
    def get(self):
    # Generate the deployment details dynamically
        deployment_details = generate_deployment_details()
        return jsonify(deployment_details)
