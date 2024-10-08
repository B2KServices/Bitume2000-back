from flask import Blueprint

from data.roles.models import RoleModel
from data.roles.schemas.role_schema import RoleSchema
from utils.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry

NAME = 'roles'

role_blueprint = Blueprint(NAME, __name__)
crud_role = CRUDHelper(RoleModel, RoleSchema)
role_registry = SQLAlchemyRegistry(RoleModel)

@role_blueprint.get(f'/{NAME}')
def get_roles():
    return crud_role.handle_get_all()