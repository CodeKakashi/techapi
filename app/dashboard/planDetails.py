from flask_restful import Resource
from app.dashboard.__schema__ import EditPlanSchema, UpdateColSchema

from app.db import mongo
from app.general import uniqueId, timestamp
from app.general.jwt import validate_auth
from flask import request

from app.libs import getUserSnippet


mdb = mongo.db


class PlanDetails(Resource):
    @validate_auth()
    def get(self, suid, suser):
        planDetails = []
        planDetailMeta = mdb.listPlans.find({"status": "active"})

        for planDetail in planDetailMeta:
            planDetails.append(planDetail)

        return {
            "status": 1,
            "class": "success",
            "message": "Available Plans",
            "payload": {"planDetails": planDetails},
        }


class CollectionList(Resource):
    @validate_auth()
    def get(self, suid, suser):
        pList = []
        clist = []
        userList = suser.get("userList")

        for user in userList:
            if user:
                dues = []
                uid = user["key"]
                onGoingdue = user["onGoingDue"]
                if len(user["pendingDues"]) > 0:
                    pendingDues = user["pendingDues"]
                    dues.extend(pendingDues)
                dues.append(onGoingdue)
                for due in dues:
                    # get pending Amount and lease amount
                    clientMeta = mdb.users.find_one(
                        {"_id": uid}, {"lAmount": 1, "pendingAmount": 1}
                    )
                    dueMeta = mdb.pDues.find_one(
                        {"allotedTo": suid, "uid": uid, "dueNumber": due}
                    )
                    if clientMeta == None:
                        break
                    else:
                        # Add in the Due Meta
                        dueMeta["lAmount"] = clientMeta["lAmount"]
                        dueMeta["pendingAmount"] = clientMeta["pendingAmount"]

                    # Append in the Pending List
                    pList.append(dueMeta)

        cCursor = mdb.cList.find({"entryBy": suid})

        for list in cCursor:
            clist.append(list)

        return {
            "status": 1,
            "class": "success",
            "message": "Collection List",
            "payload": {
                "collectionList": {
                    "pList": pList,
                    "cList": clist,
                }
            },
        }


class UpdateCollectionList(Resource):
    @validate_auth()
    def post(self, suid, suser):
        print("suser: ", suser)
        input = request.get_json(silent=True)
        form = UpdateColSchema().load(input)
        showForm = form.get("showForm", False)
        reason = form.get("reason", "")
        paymentMode = form.get("paymentMode", "")
        onGoingDue = form.get("onGoingDue", "")
        uid = form.get("uid", "")
        generatedPayment = form.get("generatedPayment", "")
        totalPeriod = form.get("totalPeriod", "")
        lAmount = form.get("lAmount", "")
        totalAmount = form.get("totalAmount", "")
        cName = form.get("cName", "")
        updatedGoingDue = onGoingDue + 1
        rootId = suser.get("rootId", "")

        if showForm == True:
            # Update in Completed List
            userMeta = getUserSnippet(uid, True)
            if totalAmount == lAmount:
                totalCollected = generatedPayment
            else:
                totalCollected = totalAmount - lAmount

            # Currently this logic is wrong must update
            cDue = {
                "_id": f"CD{uid}X00{onGoingDue}",
                "dueNumber": onGoingDue,
                "generatedPayment": generatedPayment,
                "paymentMode": paymentMode,
                "entryBy": suid,
                "collectorName": suser["name"],
                "uid": uid,
                "totalCollected": totalCollected,
                "totalAmount": totalAmount,
                "name": cName,
                "rootId": rootId,
                **userMeta,
            }
            mdb.cList.insert_one(cDue)

            # Update in client
            pendingAmount = lAmount - generatedPayment
            pendingPeriod = int(totalPeriod) - 1
            mdb.users.update_one(
                {"_id": uid},
                {
                    "$set": {
                        "lAmount": pendingAmount,
                        "pendingPeriod": pendingPeriod,
                        "onGoingDue": updatedGoingDue,
                    }
                },
            )

            # Unset pending list
            mdb.pDues.delete_one(
                {"uid": uid, "dueNumber": onGoingDue, "allotedTo": suid}
            )

        else:
            userMeta = getUserSnippet(uid, False)
            # Update in Pending List
            mdb.pDues.update_one(
                {"uid": uid, "dueNumber": onGoingDue, "allotedTo": suid},
                {"$set": {"reason": reason, **userMeta}},
            )
            # Update in client
            mdb.users.update_one(
                {"_id": uid}, {"$addToSet": {"pendingDues": onGoingDue}}
            )
            # Update in sub-admin pendingDues
            mdb.users.update_one(
                {"userList.key": uid, "_id": suid},
                {"$addToSet": {"userList.$.pendingDues": onGoingDue}},
            )

        # Update in sub-admin onGoingDue
        mdb.users.update_one(
            {"userList.key": uid, "_id": suid},
            {"$set": {"userList.$.onGoingDue": updatedGoingDue}},
        )

        return {
            "status": 1,
            "class": "success",
            "message": "User due has been updated successfully",
        }


class PlanUpdate(Resource):
    @validate_auth()
    def post(self, suid, suser):
        input = request.get_json(silent=True)
        form = EditPlanSchema().load(input)
        name = form.get("name", "")
        cost = form.get("cost", "")
        planId = form.get("planId", "new")
        isNewPlan = form.get("isNew", False)

        if isNewPlan and planId == "new":
            cTime = timestamp()
            prefixName = name.replace(" ", "")
            prefixName = prefixName.upper()
            _id = uniqueId(
                digit=10,
                ref={"createdAt": cTime, "createdBy": suser["name"]},
                prefix=f"{prefixName}",
                suffix=f"_{cTime}",
            )
            planExist = mdb.listPlans.find_one({"name": name, "cost": cost})
            if planExist:
                return {
                    "status": 0,
                    "class": "error",
                    "message": "Plan Already Exists",
                }
            planData = {"_id": _id, **form, "uid": suid}
            mdb.listPlans.insert_one(planData)
            return {
                "status": 1,
                "class": "success",
                "message": "Plan Added Successfully",
            }

        elif planId != "new":
            mdb.listPlans.update_one({"_id": planId}, {"$set": {**form}})
            return {
                "status": 1,
                "class": "success",
                "message": "Plan Updated Successfully",
            }
        else:
            return {
                "status": 0,
                "class": "error",
                "message": "Network error logout and try again",
            }
