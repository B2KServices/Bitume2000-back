from data.authentication.controllers import auth_manager
from data.users.models import UserModel
from marshmallow import fields, pre_load
from utils.marshmallow_utils import BaseSchema


class UserSchema(BaseSchema):
    class Meta:
        model = UserModel
        load_instance = True
        include_fk = True

    password = fields.String(required=True, load_only=True)

    @pre_load
    def hash_password(self, data, **kwargs):
        if 'password' in data:
            data['password'] = auth_manager.hash_password(data['password'])
        return data
