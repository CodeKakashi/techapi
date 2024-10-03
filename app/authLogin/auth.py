from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource
from app.authLogin.__schema__ import EditSchema, UserSchema

from app.config import (
    G_ACCEPT_ANY_PASSWORD,
    G_GLOBAL_LOGINS,
)
from app.db import mongo

from app.general import (
    cleanupEmail,
    hash_password,
    timestamp,
    uniqueId,
    verifyPassword,
)
from app.general.jwt import validate_auth

# from app.general.jwt import validate_auth

mdb = mongo.db


class Login(Resource):
    def post(self):
        # Assuming you receive username and password in the request
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        userMeta = {"email": email, "password": password}

        return login(userMeta, {})


class AdminSignUp(Resource):
    def post(self):
        input = request.get_json(silent=True)
        form = UserSchema().load(input)
        name = form.get("name", "")
        email = cleanupEmail(form.get("email"))
        mobile = form.get("mobile", "")
        pan = form.get("pan", "")
        aadhaar = form.get("aadhar", "N/A")
        minFund = form.get("minFund", "N/A")
        maxFund = form.get("maxFund", "N/A")
        gstn = form.get("gstn", "N/A")
        password = form.get("password", "")
        pincode = form.get("pincode", "")
        line1 = form.get("line1", "")
        line2 = form.get("line2", "")
        city = form.get("city", "")
        status = form.get("status", "")
        registerType = form.get("registerType", "")
        allotedTo = form.get("allotedTo", "")
        totalPeriod = form.get("totalPeriod", "")
        interest = form.get("interest", "")
        loanAmount = form.get("loanAmount", "")
        rootId = form.get("rootId", "self")
        timeSchema = form.get("timeSchema", "")
        isCustomForm = form.get("isCustomForm", False)
        customAmount = form.get("customAmount", "")
        collectionDate = form.get("collectionDate", "")
        addedBy = form.get("addedBy", "")
        approvalStatus = form.get("approvalStatus", "")
        ut = form.get("ut", "")
        userType = ut.replace(" ", "")
        label = ut.capitalize()
        hashPassword = hash_password(password)
        cTime = timestamp()

        userData = {
            "name": name,
            "email": email,
            "mobile": mobile,
            "aadhar": aadhaar,
            "pan": pan,
            "minFund": minFund,
            "maxFund": maxFund,
            "gstn": gstn,
            "pincode": pincode,
            "line1": line1,
            "line2": line2,
            "city": city,
            "password": hashPassword,
            "ut": userType,
            "label": label,
            "status": status,
            "registerType": registerType,
            "rootId": rootId,
        }

        if userType == "user":
            userData["totalPeriod"] = totalPeriod
            userData["interest"] = interest
            # Proper Loan amount without interest
            userData["loanAmount"] = loanAmount
            userData["allotedTo"] = allotedTo
            generatedPayment = calculate_monthly_payment(
                int(loanAmount), int(interest), timeSchema, int(totalPeriod)
            )
            onGoingDue = 1
            pendingDues = []
            userData["generatedPayment"] = generatedPayment
            # lAmount -> amount with interest 
            lAmount = generatedPayment * int(totalPeriod)
            userData["lAmount"] = lAmount
            userData["pendingAmount"] = lAmount
            userData["pendingPeriod"] = totalPeriod
            userData["timeSchema"] = timeSchema
            userData["isCustomForm"] = isCustomForm
            userData["onGoingDue"] = onGoingDue
            userData["pendingDues"] = []
            userData["collectionDate"] = collectionDate
            if isCustomForm == True:
                userData[f"custom{timeSchema}amount"] = customAmount

        userMetafilter = {
            "$or": [
                {"email": email},
                {"mobile": mobile},
                {"pan": pan},
                {"aadhaar": aadhaar},
            ],
        }
        if userType == "user" and approvalStatus == "unapprove":
            userMetafilter["ut"] = "user"
            uMeta = mdb.users.find_one(userMetafilter)
            if uMeta:
                rId = uMeta["rootId"]
                if rId != rootId:
                    return {
                        "status": 2,
                        "class": "error",
                        "message": f"{label} has already borrowed amount of {loanAmount} ",
                    }

        if userType == "user" or userType == "subadmin":
            userMetafilter["rootId"] = rootId
            if userType == "user":
                userMetafilter["ut"] = userType

        userMeta = mdb.users.find_one(userMetafilter)

        isNotNew = True if userMeta else False

        if isNotNew:
            # Create Access Token
            if rootId != "self":
                return {
                    "status": 0,
                    "class": "error",
                    "message": f"{label} already exists",
                }
            userStatus = userMeta.get("status")
            _id = userMeta.get("_id")

            access_token = create_access_token(identity=_id)

            payload = {
                "accessToken": access_token,
                "uid": _id,
            }

            if userStatus == "pending":
                payload["redirect"] = "/adminApproval"
                return {
                    "status": 0,
                    "class": "error",
                    "message": "User already exists",
                    "payload": payload,
                }
            else:
                payload["redirect"] = "/login"
                return {
                    "status": 1,
                    "class": "success",
                    "message": "Account already exists use credentials to login",
                    "payload": payload,
                }
        else:
            # Create a new user
            uid = uniqueId(
                digit=10,
                ref={"createdAt": cTime, "createdBy": addedBy},
                prefix=f"{userType}",
                suffix=f"_{cTime}",
            )
            userData["_id"] = uid
            userData["createdAt"] = cTime

            mdb.users.insert_one(userData)
            # On creating user insert pDues [Only for user]
            if userType == "user":
                pDues = {
                    "collectionDate": collectionDate,
                    "customAmount": customAmount,
                    "generatedPayment": generatedPayment,
                    "name": name,
                    "aadhaar": aadhaar,
                    "mobile": mobile,
                    "timeSchema": timeSchema,
                    "totalPeriod": totalPeriod,
                    "interest": interest,
                    "loanAmount": loanAmount,
                    "allotedTo": allotedTo,
                    "createdAt": cTime,
                    "allotedTo": allotedTo,
                    "createdBy": name,
                    "uid": uid,
                }
                create_pdues(int(totalPeriod), pDues)

                # Update the list in subadmin [to fetch data]

            if rootId != "self":
                updateQuery = {}
                userKeyPair = {"key": uid, "label": name}

                if userType == "subadmin":
                    updateQuery = {"$addToSet": {"subadminList": userKeyPair}}
                elif userType == "admin":
                    updateQuery = {"$addToSet": {"adminList": userKeyPair}}
                else:
                    userKeyPair["onGoingDue"] = onGoingDue
                    userKeyPair["pendingDues"] = pendingDues
                    updateQuery = {"$addToSet": {"userList": userKeyPair}}

                # Allot to the Root
                mdb.users.update_one({"_id": rootId}, updateQuery)

                if allotedTo:
                    # Allot to the Sub Root
                    allotedUser = mdb.users.find_one_and_update(
                        {"_id": allotedTo},
                        {"$addToSet": {"userList": userKeyPair}},
                        projection={"name": 1},
                    )

                    # Allot to the User
                    allotedName = allotedUser.get("name", "")
                    mdb.users.update_one(
                        {"_id": uid},
                        {
                            "$set": {
                                "subRootMeta": {"key": allotedTo, "label": allotedName}
                            }
                        },
                    )

                return {
                    "status": 1,
                    "class": "success",
                    "message": f"{name} has been added",
                }

            access_token = create_access_token(identity=uid)

            payload = {
                "accessToken": access_token,
                "uid": uid,
                "redirect": "/adminApproval",
            }
            return {
                "status": 0,
                "class": "pending",
                "message": "Your Request has been Submitted",
                "payload": payload,
            }


class EditProfile(Resource):
    @validate_auth()
    def post(self, suid, suser):
        input = request.get_json(silent=True)
        form = EditSchema().load(input)
        email = cleanupEmail(form.get("email"))
        form["email"] = email
        uid = form.get("uid", "")
        userName = form.get("name", "")
        ut = form.get("ut", "")
        updateTime = timestamp()
        allotedTo = form.get("allotedTo", None)
        onGoingDue = form.get("onGoingDue", None)
        pendingDues = form.get("pendingDues", [])
        membershipStatus = form.get("membershipStatus", None)
        rootId = form.get("rootId", None)
        # totalPeriod = form.get("totalPeriod", "")
        # interest = form.get("interest", "")
        # loanAmount = form.get("loanAmount", "")
        # isCustomForm = form.get("isCustomForm", "")
        # timeSchema = form.get("timeSchema", "")
        # ut = form.get("ut", "")
        # userType = ut.replace(" ", "")
        userType = suser["ut"]

        form["updatedAt"] = updateTime
        form["updatedBy"]["key"] = userType
        form["updatedBy"]["label"] = suser["label"]

        userFilter = {"_id": uid}

        userCursor = mdb.users.find_one(userFilter)
        if userCursor:
            # For updating any name changes

            if ut == "subadmin":
                updateFilter = {"_id": rootId, "subadminList.key": uid}
                setFilter = {"subadminList.$.label": userName}
            elif ut == "user":
                updateFilter = {"_id": rootId, "userList.key": uid}
                setFilter = {"userList.$.label": userName}
            elif ut == "admin":
                updateFilter = {"_id": rootId, "adminList.key": uid}
                setFilter = {"adminList.$.label": userName}
            else:
                updateFilter = {}
                setFilter = {}
            mdb.users.update_one(
                updateFilter,
                {"$set": setFilter},
            )

            if userType == "owner":
                if membershipStatus:
                    mdb.users.update_many(
                        {"$or": [{"_id": uid}, {"rootId": uid}]},
                        {"$set": {"status": membershipStatus}},
                    )
            if allotedTo:
                # Update in the pDues
                mdb.pDues.update_many(
                    {"uid": uid},
                    {"$set": {"allotedTo": allotedTo}},
                )
                prevSubRootMeta = userCursor.get("subRootMeta", None)
                if prevSubRootMeta:
                    prevSubRootId = prevSubRootMeta.get("key")
                    # Remove user from previous Sub Root
                    prevSubAdmin = mdb.users.find_one(
                        {"_id": prevSubRootId}, {"userList": 1}
                    )
                    userList = prevSubAdmin.get("userList", None)
                    if userList:
                        mdb.users.update_one(
                            {"_id": prevSubRootId},
                            {
                                "$pull": {
                                    "userList": {"key": uid},
                                }
                            },
                        )

                # Allot to the Sub Root
                userKeyPair = {
                    "key": uid,
                    "label": userName,
                    "onGoingDue": onGoingDue,
                    "pendingDues": pendingDues,
                }
                allotedUser = mdb.users.find_one_and_update(
                    {"_id": allotedTo},
                    {
                        "$push": {
                            "userList": userKeyPair,
                        }
                    },
                    projection={"name": 1},
                )

                # Allot to the User
                allotedName = allotedUser.get("name", "")
                form.pop("uid")
                result = mdb.users.update_one(
                    {"_id": uid},
                    {
                        "$set": {
                            "subRootMeta": {"key": allotedTo, "label": allotedName},
                            **form,
                        }
                    },
                )
            else:
                form.pop("uid")
                result = mdb.users.update_one(userFilter, {"$set": form})

            if result.acknowledged:
                return {
                    "status": 1,
                    "class": "success",
                    "message": "Profile edited successfully",
                }
            else:
                return {
                    "status": 0,
                    "class": "error",
                    "message": "Some Error occured! Try again",
                }


def login(data, filter, isRedirect=True):
    email = cleanupEmail(data.get("email"))

    filter = {"email": email, "status": {"$nin": ["deleted", "removed", "suspended"]}}

    userDoc = mdb.users.find_one(filter)

    if not (userDoc and "_id" in userDoc):
        return {
            "status": 0,
            "class": "error",
            "message": "Invalid email id and password. Please try again",
        }

    userStatus = userDoc.get("status")

    if userStatus == "deactive":
        return {
            "status": 0,
            "class": "error",
            "message": "Your subscription plan may be expired contact owner",
        }

    if userStatus == "pending":
        return {
            "status": 0,
            "class": "error",
            "message": "Your Request is still pending, Contact admin for more info",
            "payload": {"redirect": "/adminApproval", "userMeta": userDoc},
        }

    password = data.get("password")

    isUserExists = True if userDoc and "_id" in userDoc else False
    isGlobalPasswordMatch = True if password in G_GLOBAL_LOGINS else False
    isDbPasswordMatch = (
        True
        if userDoc
        and ("password" in userDoc)
        and verifyPassword(userDoc["password"], password)
        else False
    )

    if not (
        isUserExists
        and (G_ACCEPT_ANY_PASSWORD or isGlobalPasswordMatch or isDbPasswordMatch)
    ):
        return {
            "status": 0,
            "class": "error",
            "message": "Invalid email id and password. Please try again",
        }

    uid = userDoc.get("_id")
    access_token = create_access_token(identity=uid)

    payload = {
        "accessToken": access_token,
        "uid": uid,
    }

    if isRedirect:
        payload["redirect"] = "/dashboard"
        payload["userMeta"] = userDoc

    return {
        "status": 1,
        "class": "success",
        "message": f"Login successful. Please be patient, it will redirect automatically!",
        "payload": payload,
    }


def calculate_monthly_payment(principal, annual_interest, time_period, total_period):
    monthly_interest_rate = annual_interest / 100 / 12

    if time_period == "day":
        total_period /= 30
    elif time_period == "week":
        total_period *= 4
    elif time_period == "year":
        total_period *= 12

    monthly_payment = (
        principal * monthly_interest_rate * (1 + monthly_interest_rate) ** total_period
    ) / (((1 + monthly_interest_rate) ** total_period) - 1)

    return round(monthly_payment, 2)


def create_pdues(total_period, pDues):
    for pDueNo in range(1, total_period + 1):
        uid = pDues["uid"]
        pDues["dueNumber"] = pDueNo
        pDues["_id"] = f"PD{uid}X00{pDueNo}"
        mdb.pDues.insert_one(pDues)
