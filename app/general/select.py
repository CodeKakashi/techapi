import json
from flask import request as flask_request
from flask_restful import Resource, reqparse
from app.db import mongo

from app.static import G_DB_LIST_CATEGORIES

mdb = mongo.db


class LazySelect(Resource):
    def get(self, suid=None, suser=None):  # noqa: E501

        parser = reqparse.RequestParser()
        parser.add_argument(
            "category", help="Category is required", required=True, location="args"
        )
        parser.add_argument("params", required=False, location="args")
        args = parser.parse_args()

        category = args["category"]
        params = (
            json.loads(args["params"])
            if "params" in args and args["params"] is not None and args["params"] != ""
            else {}
        )

        items = []
        filter = {}

        if category in G_DB_LIST_CATEGORIES:
            dbName = G_DB_LIST_CATEGORIES[category]

            db = mdb[dbName]
            project = {"key": "$_id", "label": "$name", "_id": 0}
            match = {}
            sort = {"name": 1}

            if category == "district":
                # Return as empty when state id not passed
                filter = {}
                filter = {"stateId": "null"}
                if "stateIds" in params:
                    if not isinstance(params["stateIds"], list):
                        params["stateIds"] = [str(params["stateIds"])]

                    filter["stateId"] = {"$in": params["stateIds"]}

                match = {**match, **filter}

            query = [
                {"$match": {**match}},
                {"$sort": sort},
                {
                    "$facet": {
                        "metadata": [{"$count": "total"}, {"$addFields": {"page": 1}}],
                        "items": [
                            {"$skip": 0},
                            {"$limit": 2500},
                            {"$project": project},
                        ],
                    }
                },
            ]

            if db:
                for data in db.aggregate(query):
                    items = data["items"]

        return {
            "status": 1,
            "message": "Details fetched successfully!",
            "payload": items,
        }
