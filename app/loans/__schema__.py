from marshmallow import Schema, ValidationError, fields, validates
from marshmallow.validate import OneOf


class LoanUpdateFormSchema(Schema):
    type = fields.Str(required=True, validate=OneOf(['daily', 'weekly', 'monthly', 'yearly']), error="Type must be 'monthly'")
    lendingAmount = fields.Float(required=True, validate=lambda x: x > 0, error="Lending amount must be greater than 0")
    interest = fields.Float(required=True, validate=lambda x: x >= 0, error="Interest must be non-negative")
    startDate = fields.DateTime(required=True)
    endDate = fields.DateTime(required=True)
    fineInterest = fields.Float(required=True, validate=lambda x: x >= 0, error="Fine interest must be non-negative")
    noOfDues = fields.Number(required=True, validate=lambda x: x > 0, error="Number of loans must be greater than 0")