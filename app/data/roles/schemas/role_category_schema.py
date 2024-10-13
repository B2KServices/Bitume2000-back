from data.roles.models import RoleCategoryModel
from data.roles.schemas import RoleSchema
from marshmallow import fields
from utils.marshmallow_utils import BaseSchema


class RoleCategorySchema(BaseSchema):
    class Meta:
        model = RoleCategoryModel
        load_instance = True
        include_fk = True

    roles = fields.Nested(RoleSchema, many=True)
