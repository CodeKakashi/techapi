from collections import defaultdict
from datetime import datetime
from flask_restful import Resource

from app.db import mongo


from app.general import convertDateToCustomFormat
from app.general.jwt import validate_auth

mdb = mongo.db


class AdminCensus(Resource):
    @validate_auth()
    def get(self, suid, suser, uid, gType):
        # def get(self, uid, gType):

        adminCensus = []
        userType = suser["ut"]
        adminUid = suser["_id"]
        userCensusMeta = []
        subAdminCensusMeta = []
        subAdminMeta = {}
        subAdminRevenueMeta = []
        subAdminCollectionMeta = []

        # Pie Chart of Admin and Sub Admin count
        countFilter = {
            "$project": {
                "name": 1,
                "userListSize": {
                    "$size": {"$ifNull": ["$userList", []]}
                },  # To handle missing or null userList
                "subadminListSize": {
                    "$size": {"$ifNull": ["$subadminList", []]}
                },  # To handle missing or null subadminList
            }
        }

        # {"$sort": {"userListSize": -1}},  # Sort by userCount descending

        matchFilter = {
            "$match": {
                "ut": "admin",  # Only include documents where the type is "admin"
                "status": "active"
            }
        }

        projectionFilter = {
            "$project": {
                "name": 1,
                "userCount": "$userListSize",
                "subadminCount": "$subadminListSize",
            }
        }

        adminMeta = mdb.users.aggregate(
            [
                matchFilter,
                countFilter,
                projectionFilter,
            ]
        )

        for admin in adminMeta:
            adminCensus.append(admin)

        # Admin's User and Sub-Admin graph
        if userType == "admin":
            if gType == "statScreen":
                listAdminMeta = mdb.users.find(
                    {"rootId": adminUid},
                    {"loanAmount": 1, "name": 1, "ut": 1, "userList": 1},
                )

                for adminCenMeta in listAdminMeta:
                    if adminCenMeta["ut"] == "user":
                        loanAmount = adminCenMeta["loanAmount"]
                        adminCenMeta["loanAmount"] = int(loanAmount)
                        userCensusMeta.append(adminCenMeta)
                    else:
                        userList = adminCenMeta.get("userList", None)
                        if userList != None:
                            userCount = len(userList)
                            adminCenMeta.pop("userList")
                            adminCenMeta["userCount"] = userCount
                        subAdminCensusMeta.append(adminCenMeta)

            # Sub Admin's Revenue
            cListAdminMeta = mdb.cList.find(
                {"rootId": adminUid},
                {"totalCollected": 1, "collectorName": 1, "entryBy": 1},
            )

            for cUser in cListAdminMeta:
                entryBy = cUser["entryBy"]
                collectorName = cUser["collectorName"]
                totalCollected = cUser["totalCollected"]

                # If the entryBy is already in the dictionary, add to its total
                if entryBy in subAdminMeta:
                    subAdminMeta[entryBy]["totalCollected"] += totalCollected
                else:
                    # Initialize with current totalCollected if entryBy not found
                    subAdminMeta[entryBy] = {
                        "name": collectorName,
                        "totalCollected": totalCollected,
                    }
            subAdminRevenueMeta = convertDictToList(subAdminMeta)

        # Sub Admin Collection Graph

        if userType == "subadmin":
            subAdminCollectionList = mdb.cList.find(
                {"entryBy": suid}, {"createdAt": 1, "entryBy": 1, "totalCollected": 1}
            )

            subAdminCollectionMeta = groupByDate(subAdminCollectionList)

        # Admin Revenue Graph
        listAdmins = mdb.users.find({"ut": "admin"}, {"_id": 1, "name": 1})

        adminIds = []
        results = []

        for admin in listAdmins:
            adminId = admin.get("_id", None)
            adminName = admin.get("name", None)
            if adminId != None:
                adminIds.append({"_id": adminId, "name": adminName})

        for adminId in adminIds:
            # MongoDB aggregation pipeline
            pipeline = [
                {
                    # Match documents where rootId matches the current adminId
                    "$match": {"rootId": adminId["_id"]}
                },
                {
                    # Group by rootId and sum up the loanAmount
                    "$group": {
                        "_id": "$rootId",  # Group by rootId
                        "totalLoanAmount": {
                            "$sum": {"$toInt": "$loanAmount"}
                        },  # Sum loanAmount after converting to int
                    }
                },
                {
                    # Add admin name and format the output structure
                    "$addFields": {
                        "rootId": adminId["_id"],
                        "name": adminId["name"],
                        "loan_amount": "$totalLoanAmount",
                    }
                },
                {
                    # Format the final output
                    "$project": {"_id": 0, "rootId": 1, "name": 1, "loan_amount": 1}
                },
            ]

            # Execute the aggregation query
            result = mdb.users.aggregate(pipeline)

            # Append the result to the results list
            if result:
                results.extend(result)

        return {
            "status": 1,
            "class": "success",
            "message": "Available Plans",
            "payload": {
                "censusMeta": adminCensus,
                "adminRevenueMeta": results,
                "subAdminRevenueMeta": subAdminRevenueMeta,
                "userCensusMeta": userCensusMeta,
                "subAdminCensusMeta": subAdminCensusMeta,
                "subAdminCollectionMeta": subAdminCollectionMeta,
            },
        }


class ClientSchedule(Resource):
    @validate_auth()
    def get(self, suid, suser, uid):
        if uid == "error":
            return {
                "status": 0,
                "class": "error",
                "message": "Something went wrong",
                "payload": {"msg": "Something went wrong"},
            }
        else:
            pDues_data = mdb.pDues.find({"uid": uid})
            cList_data = mdb.cList.find({"uid": uid})

            # Initialize output variables
            dueMeta = []
            totalPeriod = 0
            collectedBy = "Yet to be"
            collectedOn = "Yet to be"

            # Process pDues data
            for pdue in pDues_data:
                dueNumber = pdue.get("dueNumber")
                generatedPayment = pdue.get("generatedPayment")
                totalPeriod = pdue.get("totalPeriod")

                # Check if due number exists in cList to determine payment status
                payment_status = "unpaid"

                # Append to dueMeta list
                dueMeta.append(
                    [
                        f"Due {int(dueNumber)}",
                        str(generatedPayment),
                        payment_status,
                        collectedBy,
                        collectedOn,
                    ]
                )

            for cdue in cList_data:
                dueNumber = cdue.get("dueNumber")
                generatedPayment = cdue.get("generatedPayment")
                collectedOn = cdue.get("createdAt")
                collectedBy = cdue.get("collectorName", "Yet to be")
                updatedDate = convertDateToCustomFormat(str(collectedOn))

                # Check if due number exists in cList to determine payment status
                payment_status = "paid"

                # Append to dueMeta list
                dueMeta.append(
                    [
                        f"Due {dueNumber}",
                        str(generatedPayment),
                        payment_status,
                        collectedBy,
                        updatedDate,
                    ]
                )

            dueMeta.sort(key=lambda x: int(float(x[0].split()[1])))

            # Prepare final output
            dueMetaList = {"dueMeta": dueMeta, "totalPeriod": int(totalPeriod)}

            return {
                "status": 1,
                "class": "success",
                "message": "Client Debt Schedule",
                "payload": dueMetaList,
            }


def convertDictToList(input_dict):
    # Extract the values from the input dictionary and convert to a list
    result = list(input_dict.values())
    return result


def groupByDate(data):
    # Dictionary to store collections grouped by date (YYYY/MM)
    grouped_data = defaultdict(int)

    # Iterate through each entry in the data
    for entry in data:
        # Extract the date and totalCollected
        created_at = entry["createdAt"]  # Assuming this is already a datetime object
        total_collected = entry["totalCollected"]

        # Format the date as YYYY/MM
        date_key = f"{created_at.year}/{created_at.month:02d}"

        # Sum the totalCollected for the same YYYY/MM date_key
        grouped_data[date_key] += total_collected

    # Convert grouped data to the desired list of dictionaries
    result = [{"date": date, "totalCollection": total} for date, total in grouped_data.items()]

    # Sorting by year and month
    result.sort(key=lambda x: datetime.strptime(x["date"], "%Y/%m"))

    return result

