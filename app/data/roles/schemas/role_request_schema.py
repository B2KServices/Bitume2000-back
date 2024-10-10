from data.roles.models import RoleModel
from data.roles.models.role_request_model import RoleRequestModel
from utils.marshmallow_utils import BaseSchema


class RoleRequestSchema(BaseSchema):
    class Meta:
        model = RoleRequestModel
        load_instance = True
        include_fk = True