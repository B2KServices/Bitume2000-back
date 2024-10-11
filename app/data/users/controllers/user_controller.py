from http import HTTPStatus

from discord import Member
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError

from config import config, BaseConfig
from data.roles.models import RoleModel
from data.roles.schemas import RoleSchema
from data.users.models import UserModel
from data.users.schemas import UserSchema
from flask import Blueprint, request

from errors import BaseCustomError
from setup import bot
from utils.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry

NAME = 'users'

users_blueprint = Blueprint(f'{NAME}_blueprint', __name__)
user_registry = SQLAlchemyRegistry(UserModel)
users_crud = CRUDHelper(UserModel, UserSchema)
role_registry = SQLAlchemyRegistry(RoleModel)


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
    user: UserModel = user_registry.get_one_by_id_or_fail(id_user)
    return RoleSchema(many=True).dump(user.roles), HTTPStatus.OK

@users_blueprint.post(f'/{NAME}/me/roles')
@jwt_required()
async def update_role():
    id_user = get_jwt_identity()
    data = request.get_json()
    id_role = data.get('id_role', None)
    adding_role = data.get('adding_role', None)
    user = user_registry.get_one_by_id_or_fail(id_user)
    if id_role or adding_role is not None:
        role = role_registry.get_one_by_id_or_fail(id_role)
        if adding_role is True:
            bot.add_role_to_member(config.GUILD_ID, user.id_discord, role.id_discord)
            user.roles.append(role)
        else:
            bot.remove_role_from_member(config.GUILD_ID, user.id_discord, role.id_discord)
            user.roles.remove(role)
        user = user_registry.update_one(user)
        return RoleSchema(many=True).dump(user.roles), HTTPStatus.OK
    raise ValidationError('missing id_role or adding_role')

@users_blueprint.get(f'/{NAME}/update-role')
async def update_roles():
    users = user_registry.get_all()
    for user in users:
        user: UserModel = user
        id_discord = user.id_discord
        roles = await bot.get_roles_from_member(config.GUILD_ID, id_discord)
        for role in roles:
            try:
                role: RoleModel = role_registry.get_one_or_fail_where(id_discord=str(role.id))
                user.roles.append(role)
            except BaseCustomError:
                pass

        user_registry.update_one(user)

    return users_crud.handle_get_all(), HTTPStatus.OK