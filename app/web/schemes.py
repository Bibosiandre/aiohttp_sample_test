from marshmallow import Schema, fields


class ResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict()
