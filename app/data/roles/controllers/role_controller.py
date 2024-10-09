from discord import Role
from flask import Blueprint, request
from pygments.util import docstring_headline

from config import config
from data.roles.models import RoleModel, RoleCategoryModel
from data.roles.schemas.role_category_schema import RoleCategorySchema
from data.roles.schemas.role_schema import RoleSchema
from managers.swagger_manager.doc_decorator import swagger
from setup import bot, docs
from utils.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry

NAME = 'roles'

role_blueprint = Blueprint(NAME, __name__)
crud_role = CRUDHelper(RoleModel, RoleSchema)
crud_category = CRUDHelper(RoleCategoryModel, RoleCategorySchema)
role_registry = SQLAlchemyRegistry(RoleModel)
category_registry = SQLAlchemyRegistry(RoleCategoryModel)

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