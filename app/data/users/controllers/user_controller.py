from http import HTTPStatus


from data.users.models import UserModel, UserProjectModel
from data.users.schemas import UserSchema
from data.users.schemas.user_project_schema import UserProjectSchema
from errors import BaseCustomError
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from setup import docs
from utils.crud_helper import CRUDHelper
from utils.registry import SQLAlchemyRegistry

NAME = 'users'

users_blueprint = Blueprint(f'{NAME}_blueprint', __name__)
user_registry = SQLAlchemyRegistry(UserModel)
user_project_registry = SQLAlchemyRegistry(UserProjectModel)
users_crud = CRUDHelper(UserModel, UserSchema)

