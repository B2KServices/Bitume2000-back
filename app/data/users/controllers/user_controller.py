from http import HTTPStatus

from discord import Member

from data.users.models import UserModel
from data.users.schemas import UserSchema
from flask import Blueprint

from setup import bot
from utils.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry

NAME = 'users'

users_blueprint = Blueprint(f'{NAME}_blueprint', __name__)
user_registry = SQLAlchemyRegistry(UserModel)
users_crud = CRUDHelper(UserModel, UserSchema)

@users_blueprint.get(f'/{NAME}/update-discord')
async def update_users():
    if len(user_registry.get_all()) > 0:
        return 'nope', HTTPStatus.BAD_REQUEST
    members = await bot.get_members_from_guild(382938797442334720)
    for member in members:
        member: Member = member
        user = UserModel()
        user.id_discord = member.id
        user.username = member.name
        user.avatar_url = member.avatar.url
        user_registry.create_one(user)
    return users_crud.handle_get_all()
