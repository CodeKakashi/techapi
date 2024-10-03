from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from app.db import mongo

# Now you can directly access mdb from the instance
mdb = mongo.db


def validate_auth(optional=False):
    def decorator(fn):
        @jwt_required(optional=optional)
        @wraps(fn)
        def wrapper(*args, **kwargs):
            suid = None
            suser = None
            try:
                identity = None  # Initialize identity to None
                if optional:
                    # Check if JWT token is present in the request headers
                    auth_header = request.headers.get('Authorization')
                    if auth_header:
                        # Extract JWT token from the Authorization header
                        identity = get_jwt_identity()
                        if identity is None:
                            return jsonify({'message': 'Invalid JWT token'}), 401
                else:
                    # Get the identity after validation
                    identity = get_jwt_identity()
            except Exception as e:
                return jsonify({'message': str(e)}), 500
            
            if identity:
                suid = identity
                if suid:
                    suser = mdb.users.find_one(suid)
            return fn(*args, suid=suid, suser=suser, **kwargs)
        return wrapper
    return decorator


# def auth_required(**kwargs):
#     amac = kwargs.get("amac")
#     isOptional = kwargs.get("isOptional", False)

#     def _decorator(fn):
#         @jwt_required(optional=isOptional)
#         @wraps(fn)
#         def wrapper(*args, **kwargs):
#             verify_jwt_in_request(optional=isOptional)

#             suid = get_jwt_identity()

#             if isOptional and not suid:
#                 return fn(*args, **kwargs, suid=None, suser=None)

#             suser = getAuthUser(suid)
#             if not(suser and "_id" in suser):
#                 return {
#                     "status": 0,
#                     "message": "Invalid Access. Please login again",
#                     "payload": {
#                         "redirectUrl": "/user/login",
#                         "logout": True
#                     }
#                 }, 403

#             if amac and not validateAccess(suid, suser, amac):
#                 return {
#                     "status": 0,
#                     "message": "Unauthorized Access",
#                     "payload": {"redirectUrl": "/"}
#                 }, 401

#             return fn(*args, **kwargs, suid=suid, suser=suser)
#         return wrapper

#     return _decorator