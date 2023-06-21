from marshmallow import Schema, fields

from app.web.schemes import ResponseSchema


class UserSchema(Schema):
    email = fields.Str(required=True)


class UserAddSchema(UserSchema):
    email = fields.Str(required=True)


class UserSchema(UserAddSchema):
    id = fields.UUID(required=True)


class UserGetRequestSchema(Schema):
    id = fields.UUID(required=True)


class UserGetSchema(Schema):
    user = fields.Nested(UserSchema)


class GetUserResponseSchema(ResponseSchema):
    data = fields.Nested(UserGetSchema)


class ListUsersSchema(Schema):
    users = fields.Nested(UserSchema, many=True)


class ListUsersResponseSchema(ResponseSchema):
    data = fields.Nested(ListUsersSchema)
