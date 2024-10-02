from http import HTTPStatus


from data.users.models import UserModel
from data.users.schemas import UserSchema
from flask import Blueprint
from utils.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry

NAME = 'users'

users_blueprint = Blueprint(f'{NAME}_blueprint', __name__)
user_registry = SQLAlchemyRegistry(UserModel)
users_crud = CRUDHelper(UserModel, UserSchema)

