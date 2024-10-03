from marshmallow import Schema, fields

from app.authLogin.__schema__ import LazySelectSchema


class ComplaintSchema(Schema):
    name = fields.String()
    issue = fields.String()
    uid = fields.String()
    ut = fields.String()
    updatedBy = fields.Nested(LazySelectSchema, required=True)


class QuotationSchema(Schema):
    field = fields.String()
    technology = fields.String()
    whatsappNumber = fields.String()


class DeleteClientSchema(Schema):
    id = fields.String(required=True)
    status = fields.String(required=True)


class EditPlanSchema(Schema):
    name = fields.String()
    description = fields.String()
    cost = fields.String()
    trialPeriodDays = fields.String()
    status = fields.String()
    planId = fields.String()
    updatedBy = fields.Nested(LazySelectSchema, required=True)
    updatedUid = fields.String()
    _id = fields.String()
    isNew = fields.Bool()

class UpdateColSchema(Schema):
    showForm = fields.Bool(allow_none=True)
    reason = fields.Str(allow_none=True)
    paymentMode = fields.Str(allow_none=True)
    uid = fields.Str(allow_none=True)
    onGoingDue = fields.Int(allow_none=True)
    amountCollected = fields.Str(allow_none=True)
    generatedPayment = fields.Int(allow_none=True)
    totalPeriod = fields.Str(allow_none=True)
    cName = fields.Str(allow_none=True)
    totalAmount = fields.Int(allow_none=True)
    lAmount = fields.Int(allow_none=True)