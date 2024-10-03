from flask import request
from flask_restful import Resource

from app.authLogin.__schema__ import ApproveAdminSchema, UserSchema
from app.general import hash_password, uniqueId
from app.db import mongo
from app.general.jwt import validate_auth
from app.libs import getUserSnippet
from app.static import G_CLIENT_TYPE_LABELS

mdb = mongo.db


class CreateUser(Resource):
    def post(self, uid):
        input = request.get_json(silent=True)
        form = UserSchema().load(input)

        registerType = form["registerType"]
        password = form["password"]
        hashPassword = hash_password(password)

        form.pop("password", None)

        isNewUser = True if uid == "new" else False


        if isNewUser:
            _id = f"{G_CLIENT_TYPE_LABELS[registerType]['key']}X{uniqueId(8)}"
            userMeta = getUserSnippet(_id, isNewUser)
            userItem = {
                "_id": _id,
                **form,
                "password": hashPassword,
                **userMeta,
            }

            mdb.users.insert_one(userItem)

        return {
            "status": 1,
            "class": "success",
            "message": "Success",
            "payload": {"email": form["email"], "password": password},
        }


class ApprovalList(Resource):
    @validate_auth()
    def get(self, suid, suser, approvalType):
        pendingUsers = []
        userFilter = {"ut": "admin"}
        if approvalType == "pending":
            userFilter["status"] = "pending"
        elif approvalType == "rejected":
            userFilter["status"] = "rejected"
        elif approvalType == "deleted":
            userFilter["status"] = "delete"
        else:
            userFilter["status"] = {"$ne": "active"}

        users = mdb.users.find(userFilter)

        for user in users:
            updatedAt = user.get("updatedAt")
            deleteMeta = user.get("deleteMeta")
            user.pop("password")
            user.pop("deleteMeta") if deleteMeta else None
            user.pop("updatedAt") if updatedAt else None
            pendingUsers.append(user)

        if len(pendingUsers) > 0:
            return {
                "status": 1,
                "class": "success",
                "message": "Success",
                "payload": {"pendingUsers": pendingUsers},
            }
        else:
            return {
                "status": 0,
                "class": "error",
                "message": "No Users Found",
            }


class ApproveAdmin(Resource):
    @validate_auth()
    def post(self, suid, suser):
        input = request.get_json(silent=True)
        form = ApproveAdminSchema().load(input)
        adminId = form.get("uid", "")
        status = form.get("status", "")
        userMeta = getUserSnippet(suid, False)

        adminApproval = mdb.users.find_one_and_update(
            {"_id": adminId},
            {"$set": {"status": status, "rootId": suid, **userMeta}}
        )

        name = adminApproval.get("name", "")

        if status == "active":
            userKeyPair = {"key": adminId, "label": name}

            mdb.users.update_one(
                {"_id": suid},
                {"$addToSet": {"adminList": userKeyPair}}
            )

        if adminApproval is not None: 
            status = status.capitalize()
            return {
                "status": 1,
                "class": "success",
                "message": f"User id {adminId} has been {status}",
            }

        else:
            return {
                "status": 0,
                "class": "error",
                "message": "Try again",
                "payload": {"redirect": "/dashboard"},
            }
