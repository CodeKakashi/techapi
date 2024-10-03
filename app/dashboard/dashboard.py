from flask_restful import Resource
from flask import request
from app.dashboard.__schema__ import DeleteClientSchema

from app.db import mongo
from app.general.jwt import validate_auth
from app.libs import getUserSnippet

mdb = mongo.db


class Dashboard(Resource):
    @validate_auth()
    def get(self, suid, suser):

        pendingUserCount = mdb.users.count_documents(
            {"status": "pending", "ut": "admin"}
        )
        admins = []
        users = []
        subAdmins = []

        adminList = suser.get("adminList", [])
        subadminList = suser.get("subadminList", [])
        userList = suser.get("userList", [])

        requiredDetials = {"name": 1, "email": 1, "mobile": 1, "ut": 1, "label": 1}

        # Extract user IDs from all lists
        user_ids = [item["key"] for item in adminList + subadminList + userList if item]

        # Fetch user details in a single query
        user_cursor = mdb.users.find(
            {"_id": {"$in": user_ids}, "status": "active"}, requiredDetials
        )

        # Populate the respective lists
        for user_meta in user_cursor:
            if user_meta["_id"] in [item["key"] for item in adminList]:
                admins.append(user_meta)
            elif user_meta["_id"] in [item["key"] for item in subadminList]:
                subAdmins.append(user_meta)
            elif user_meta["_id"] in [item["key"] for item in userList]:
                users.append(user_meta)

        return {
            "status": 1,
            "class": "success",
            "message": "Account already exists use credentials to login",
            "payload": {
                "userMeta": suser,
                "pendingUserCount": pendingUserCount,
                "listUserData": {
                    "users": users,
                    "subAdmins": subAdmins,
                    "admins": admins,
                },
            },
        }


class ClientDetails(Resource):
    @validate_auth()
    def get(self, suid, suser, ut):

        userType = getUserType(ut)
        listClients = []

        clientCursor = mdb.users.find(
            {"ut": userType, "rootId": suid, "status": "active"}
        )

        for client in clientCursor:
            deleteMeta = client.get("deleteMeta", None)
            updatedAt = client.get("updatedAt", None)
            client.pop("password")
            client.pop("deleteMeta") if deleteMeta else None
            client.pop("updatedAt") if updatedAt else None
            listClients.append(client)

        return {
            "status": 1,
            "class": "success",
            "message": f"Available {ut}",
            "payload": {"listClients": listClients},
        }


class DeleteClient(Resource):
    @validate_auth()
    def post(self, suid, suser):
        input = request.get_json(silent=True)
        form = DeleteClientSchema().load(input)
        _id = form.get("id", "")
        status = form.get("status", "")
        userMeta = getUserSnippet(False)
        deleteUser = mdb.users.update_one(
            {"_id": _id},
            {"$set": {"status": status, "deletedBy": suid, "deleteMeta": {**userMeta}}},
        )
        if deleteUser.modified_count > 0:
            status = status.capitalize()
            return {
                "status": 1,
                "class": "success",
                "message": f"User id {_id} has been {status}d",
            }

        else:
            return {
                "status": 0,
                "class": "error",
                "message": "Try again",
            }


def getUserType(ut):
    if ut == "manageAdmins":
        return "admin"
    elif ut == "manageSubAdmins":
        return "subadmin"
    else:
        return "user"
