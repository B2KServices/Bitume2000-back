from http import HTTPStatus

from discord import Role
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from marshmallow import ValidationError
from pygments.util import docstring_headline

from config import config
from data.roles.models import RoleModel, RoleCategoryModel
from data.roles.models.role_request_model import RoleRequestModel
from data.roles.schemas.role_category_schema import RoleCategorySchema
from data.roles.schemas.role_request_schema import RoleRequestSchema
from data.roles.schemas.role_schema import RoleSchema
from data.users.controllers.user_controller import user_registry
from data.users.models import UserModel
from errors import BaseCustomError
from managers.swagger_manager.doc_decorator import swagger
from setup import bot, docs
from utils.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry

NAME = 'roles'

role_blueprint = Blueprint(NAME, __name__)
crud_role = CRUDHelper(RoleModel, RoleSchema)
request_role_registry = SQLAlchemyRegistry(RoleRequestModel)
crud_category = CRUDHelper(RoleCategoryModel, RoleCategorySchema)
role_registry = SQLAlchemyRegistry(RoleModel)
category_registry = SQLAlchemyRegistry(RoleCategoryModel)
user_registry = SQLAlchemyRegistry(UserModel)

@role_blueprint.get(f'/{NAME}')
def get_roles():
    return crud_role.handle_get_all()

@swagger(
    body={'description': 'Create a new role', 'content': RoleCategorySchema},
    responses={
        200: {'description': 'Success', 'content': RoleCategorySchema},
    }
)
@role_blueprint.post(f'/{NAME}/categories')
def create_role_category():
    data = request.get_json()
    return crud_category.handle_post(data)

@role_blueprint.post(f'/{NAME}/request')
@jwt_required()
async def request_role():
    id_user = get_jwt_identity()
    data = request.get_json()
    data['id_user'] = id_user
    user: UserModel = user_registry.get_one_by_id_or_fail(id_user)
    role_request = request_role_registry.create_one(RoleRequestSchema().load(data))
    bot.send_message(f'{user.username} a fait la demande pour le role {role_request.name} pour la categorie {role_request.role_category.name}')
    return RoleRequestSchema().dump(role_request), HTTPStatus.OK


@role_blueprint.post(f'/{NAME}/approve')
@jwt_required()
async def approve_role_request():
    id_request = request.get_json().get('id_request', None)
    if id_request:
        role_request: RoleRequestModel = request_role_registry.get_one_by_id_or_fail(id_request)
        user: UserModel = user_registry.get_one_by_id_or_fail(role_request.id_user)
        user.approved_role_requests.append(role_request)
        if role_request not in user.approved_role_requests:
            user.approved_role_requests.append(role_request)
            user = user_registry.update_one(user)
        else:
            raise BaseCustomError('Role request already approved')
        if len(role_request.approved_users) >= 2:
            role_discord = await bot.create_role(config.GUILD_ID, role_request.name, role_request.role_category.color)
            role_model = RoleModel(
                id_discord=role_discord.id,
                name=role_request.name,
                id_role_category=role_request.id_role_category
            )
            role_model = role_registry.create_one(role_model)
            request_role_registry.delete_one_or_fail(role_request)
            bot.send_message(f'Le role {role_request.name} a été créé pour la categorie {role_request.role_category.name}', config.ANNOUNCEMENT_CHANNEL_ID)
            return RoleSchema().dump(role_model), HTTPStatus.OK
        return RoleRequestSchema().dump(role_request), HTTPStatus.OK




@role_blueprint.get(f'/{NAME}/categories')
def get_role_categories():
    return crud_category.handle_get_all()

@role_blueprint.get(f'/{NAME}/categories/update-discord')
def update_categories():
    categories = {'Position': '#4a8b29',
           'IRL': '#00FF00',
           'Autres': '#F1C232',
           'Stratégie': '#9900FF',
           'Réflexion': '#00FFFF',
           'Combat': '#E91E1E',
           'Party Games': '#FF9900',
           'Survie/ Aventure': '#CCCCCC',
           'Course': '#0161FF',
           'FPS': '#00DE8C'
           }
    for key, value in categories.items():
        category_model = RoleCategoryModel()
        category_model.name = key,
        category_model.color = value.lower()
        category_registry.create_one(category_model)
    return crud_category.handle_get_all()

@role_blueprint.get(f'/{NAME}/update-discord')
async def update_discord():
    roles = await bot.get_role_from_guild(config.GUILD_ID)
    categories: list[RoleCategoryModel] = category_registry.get_all()
    for role in roles:
        role: Role = role
        for category in categories:
            if category.color == str(role.color):
                role_model = RoleModel()
                role_model.id_discord = role.id
                role_model.name = role.name
                role_model.id_role_category = category.id_role_category
                category_registry.create_one(role_model)
    return crud_role.handle_get_all()



docs.register_function(create_role_category, role_blueprint)