from http import HTTPStatus

from discord import Member
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from config import config
from data.roles.models import RoleModel
from data.roles.schemas import RoleSchema
from data.users.models import UserModel
from data.users.models.user_role_model import UserRoleModel
from data.users.schemas import UserSchema
from flask import Blueprint, request

from setup import bot
from utils.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry
from utils.request_default_responses import DefaultResponse

NAME = 'users'

users_blueprint = Blueprint(f'{NAME}_blueprint', __name__)
user_registry = SQLAlchemyRegistry(UserModel)
users_crud = CRUDHelper(UserModel, UserSchema)
user_role_registry = SQLAlchemyRegistry(UserRoleModel)
roles_registry = SQLAlchemyRegistry(RoleModel)

@users_blueprint.get(f'/{NAME}/update-discord')
async def update_users():
    if len(user_registry.get_all()) > 0:
        return 'nope', HTTPStatus.BAD_REQUEST
    members = await bot.get_members_from_guild(config.GUILD_ID)
    for member in members:
        member: Member = member
        user = UserModel()
        user.id_discord = member.id
        user.username = member.name
        user.avatar_url = member.avatar.url
        user_registry.create_one(user)
    return users_crud.handle_get_all()

@users_blueprint.get(f'/{NAME}')
def get_all():
    return users_crud.handle_get_all()

@users_blueprint.get(f'/{NAME}/me')
@jwt_required()
def get_me():
    id_user = get_jwt_identity()
    return users_crud.handle_get(id_user)

@users_blueprint.patch(f'/{NAME}/me')
@jwt_required()
def update_user(id_user):
    data = request.get_json()
    return users_crud.handle_patch(id_user, data)

@users_blueprint.get(f'/{NAME}/me/roles')
@jwt_required()
def get_roles():
    id_user = get_jwt_identity()
    roles_id = user_role_registry.get_all_where(id_user=id_user)
    roles = []
    for role_id in roles_id:
        roles.append(roles_registry.get_one_by_id_or_fail(role_id))
    return RoleSchema(many=True).dump(roles), HTTPStatus.OK

@users_blueprint.post(f'/{NAME}/me/roles')
@jwt_required()
def add_role():
    id_user = get_jwt_identity()
    data = request.get_json()
    id_role = data.get('id_role', None)
    if id_role:
        user_role = UserRoleModel()
        user_role.id_user = id_user
        user_role.id_role = id_role
        user_role_registry.create_one(user_role)
        return DefaultResponse.success('Role added'), HTTPStatus.OK
    raise ValidationError('missing id_role')

@users_blueprint.delete(f'/{NAME}/me/roles')
@jwt_required()
def remove_role():
    id_user = get_jwt_identity()
    data = request.get_json()
    id_role = data.get('id_role', None)
    if id_role:
        user_role = user_role_registry.get_one_or_fail_where(id_user=id_user, id_role=id_role)
        user_role_registry.delete_one_or_fail(user_role)
        return DefaultResponse.success('Role removed'), HTTPStatus.OK
    raise ValidationError('missing id_role')