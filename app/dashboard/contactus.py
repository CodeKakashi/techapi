from flask_restful import Resource
from app.dashboard.__schema__ import QuotationSchema

from app.db import mongo
from app.general import timestamp, uniqueId
from app.general.jwt import validate_auth
from flask import request


mdb = mongo.db


class ContactUs(Resource):
    @validate_auth()
    def get(self, suid, suser):

        developerMeta = mdb.about.find_one({"_id": "developer_0001"})

        if developerMeta:
            return {
                "status": 1,
                "class": "success",
                "message": "Account already exists use credentials to login",
                "payload": {
                    "developerMeta": developerMeta,
                },
            }
        return {
            "status": 0,
            "class": "erro",
            "message": "Server busy",
            "payload": {
                "redirect": "/dashboard",
            },
        }


class Quotation(Resource):
    @validate_auth()
    def post(self, suid, suser):
        input = request.get_json(silent=True)
        form = QuotationSchema().load(input)
        field = form.get("field")
        technology = form.get("technology")
        whatsappNumber = form.get("whatsappNumber")
        cTime = timestamp()

        isQuotationExists = mdb.requestQuot.find_one(
            {
                "uid": suid,
                "field": field,
                "technology": technology,
                "whatsappNumber": whatsappNumber,
            }
        )

        if isQuotationExists:
            return {
                "status": 0,
                "class": "exists",
                "message": "Your response has already been saved",
            }
        else:
            _id = uniqueId(
                digit=10,
                ref={"createdAt": cTime, "createdBy": suser["name"]},
                prefix=f"{suser['ut']}",
                suffix=f"_{cTime}",
            )
            quoatationData = {"_id": _id, **form, "uid": suid}
            mdb.requestQuot.insert_one(quoatationData)

            return {
                "status": 1,
                "class": "success",
                "message": "Your response has saved, Team will contact you",
            }
