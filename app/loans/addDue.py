from datetime import datetime, timedelta, timezone
from flask import request
from flask_restful import Resource
from app.loans.__schema__ import LoanUpdateFormSchema
from app.general import getDayEnd, getDayStart, timestamp, uniqueId, uniqueSerialNumber
from app.general.jwt import validate_auth
from app.libs import getUserSnippet
from app.db import mongo
from app.general.constants import loanTypeDaysMap
from app.static import G_DT_REV_HYP_V3

mdb = mongo.db

# {
#     "_id": "OD001",
#     "type": "monthly",
#     "lendedAmount": 50000.00, // Without interest rate
#     "totalAmount": 55000.00, // Interest included
#     "pendingAmount": 10000.00, // Remaining amount in total amount
#     "noOfDues": 12,
#     "startDate": "2024-01-01T14:37:24.135Z",
#     "endDate": "2025-01-01T14:37:24.135Z",
#     "interest": 10,
#     "fineInterest": 5,
#     "uid": "USERID001",
#     "lid": "LE001",
#     "dueStatus": "pending",
#     "status": "active",
#     "createdAt" : "2024-01-01T14:37:24.135Z",
#     "createdUid" : "CDPNPZQ",
#     "createdBy" : {
#         "sut" : "suba",
#         "sname" : "Sample Guy 1"
#     },
#     "createdIp" : {
#         "ip" : "117.213.167.117",
#         "browser" : "Chrome",
#         "rua" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#     },
#     "updatedAt" : "2024-01-01T14:37:24.135Z",
#     "updatedUid" : "CDPNPZQ",
#     "updatedBy" : {
#         "sut" : "suba",
#         "sname" : "Sample Guy 1"
#     },
#     "updatedIp" : {
#         "ip" : "117.213.167.117",
#         "browser" : "Chrome",
#         "rua" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
#     },
# }

# {
#         "_id": "D001",
#         "dueDate": "2024-01-05T14:37:24.135Z",
#         "dueAmount": 4166.66,
#         "totalAmount": 4582.66,
#         "dueStatus": "completed",
#         "collectedAt": "2024-01-01T14:37:24.135Z",
#         "collectedUid": "CDPNPZQ",
#         "collectedBy": {
#             "sut": "suba",
#             "sname": "Sample Guy 1"
#         },
#         "collectedAmount": 4166.66,
#         "odId": "OD001",
#         "uid": "sample",
#         "lid": "LE001"
#     },


class LoanUpdate(Resource):
    # @validate_auth()
    def post(self, loanId):
        suid = None
        suser = {}
        input = request.get_json(silent=True)
        form = LoanUpdateFormSchema().load(input)
        
        isNewLoan = True if loanId == "new" else False
        userMeta = getUserSnippet(suid, isNewLoan, sby=suser)

        if isNewLoan:
            loanId = uniqueId(digit=5, prefix="LOANX", suffix=f"X{timestamp()}")

            loanItem = {
                **form,
                '_id': loanId,
                'lid': suid,
                'uid': 'userId',
                **userMeta
            }

            mdb.loans.insert_one(loanItem)
            generateDues(suid, suser, None, loanId, form)

        return {
            'status': 1,
            'class': 'success',
            'message': 'Loan details updated successfully'
        }


def generateDues(suid, suser, uid, loanId, form):
    startDate = getDayStart(form['startDate'])
    endDate = getDayEnd(form['endDate'])

    deltaDays = loanTypeDaysMap[form['type']]
    delta = timedelta(days=deltaDays)

    currentDate = startDate
    dues = []

    dueDates = []
    while currentDate < endDate:
        next = currentDate + delta
        nextUtc = getDayEnd(next.replace(tzinfo=timezone.utc)) 
        dueDates.append(nextUtc)
        currentDate = next

    oneDueAmount = round(form['lendingAmount']/len(dueDates))
    oneDueTotalAmount = round(oneDueAmount + (oneDueAmount*(form['interest']/100)))

    for dueDate in dueDates:
        dueItem = {
            '_id': f"{loanId}X{uniqueSerialNumber('due', filter={'loanId': loanId})}",
            'dueDate':  dueDate,
            "dueAmount": oneDueAmount,
            "totalAmount": oneDueTotalAmount,
            "dueStatus": "pending",
            "uid": "sample",
            "loanId": loanId,
            "lid": suid,
            **getUserSnippet(suid, True, suser)
        }
        dues.append(dueItem)

    mdb.dues.insert_many(dues)
    mdb.loans.update_one({'_id': loanId}, {'$set': {'noOfDues': len(dueDates)}})




    