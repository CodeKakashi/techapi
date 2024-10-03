from flask import request
from flask_restful import Resource
from app.dashboard.__schema__ import ComplaintSchema
from app.general import timestamp, uniqueId
from app.general.jwt import validate_auth
from app.db import mongo


mdb = mongo.db


class ComplaintForm(Resource):
    def post(self):
        input = request.get_json(silent=True)
        form = ComplaintSchema().load(input)
        name = form.get("name", "")
        issue = form.get("issue", "")
        uid = form.get("uid", "")
        ut = form.get("ut", "")
        updatedBy = form.get("updatedBy", "")
        cTime = timestamp()

        isQueryExists = mdb.complaints.find_one({"uid": uid, "issue": issue})

        if isQueryExists:
            return {
                "status": 1,
                "class": "success",
                "message": "Your Complaint has already been Submitted",
                "payload": {"redirect": "/dashboard"},
            }
        else:
            complaintID = uniqueId(
                digit=10,
                prefix=f"{form['ut']}",
                suffix=f"_{cTime}",
            )
            issueData = {
                "_id": complaintID,
                "name": name,
                "ut": ut,
                "postedBy": updatedBy,
                "issue": issue,
                "status": "notResolved",
                "datePosted": cTime,
                "history": [],
            }

            mdb.complaints.insert_one(issueData)

            return {
                "status": 1,
                "class": "success",
                "message": "Your Complaint has been Submitted",
                "payload": {"redirect": "/dashboard"},
            }
