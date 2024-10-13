from marshmallow import fields
from utils.marshmallow_utils import BaseSchema


class LoginValidationSchema(BaseSchema):
    username = fields.String(required=True)
    password = fields.String(required=True)
