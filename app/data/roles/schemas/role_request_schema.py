from marshmallow import fields

from data.roles.models.role_request_model import RoleRequestModel
from data.users.schemas import UserSchema
from utils.marshmallow_utils import BaseSchema


class RoleRequestSchema(BaseSchema):
    class Meta:
        model = RoleRequestModel
        load_instance = True
        include_fk = True

    requester = fields.Nested(UserSchema, dump_only=True)
    approved_users = fields.List(fields.Nested(UserSchema, dump_only=True))