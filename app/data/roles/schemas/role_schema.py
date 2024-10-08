from data.roles.models import RoleModel
from utils.marshmallow_utils import BaseSchema


class RoleSchema(BaseSchema):
    class Meta:
        model = RoleModel
        load_instance = True
        include_fk = True