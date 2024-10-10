from http import HTTPStatus
from time import sleep

from discord import Interaction, ButtonStyle
from discord.ui import Button

from data.authentication.schemas import LoginValidationSchema
from data.users.models import UserModel
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from errors import BaseCustomError
from errors.authentication_errors import UnauthorizedError
from managers.authentication_manager import JWTGenerationManager, PasswordAuthManager
from managers.swagger_manager.doc_decorator import swagger
from setup import docs, bot
from utils.registry import SQLAlchemyRegistry

NAME = 'auth'
auth_blueprint = Blueprint(f'{NAME}_blueprint', __name__)

auth_manager = PasswordAuthManager(UserModel)
jwt_manager = JWTGenerationManager()
user_registry = SQLAlchemyRegistry(UserModel)

@auth_blueprint.get(f'/{NAME}/admin-token')
def get_admin_token():
    return jwt_manager.generate_access_and_refresh_tokens('admin'), HTTPStatus.OK

@auth_blueprint.post(f'/{NAME}/login')
@swagger(
    body={'description': 'Les informations de connexion', 'content': LoginValidationSchema},
    responses={
        HTTPStatus.OK: {
            'description': "L'utilisateur est connecté",
            'exemple': {
                'access_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9l'
                'IiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
                'refresh_token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9l'
                'IiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c',
            },
        },
    },
)
def login():
    data = request.get_json()
    LoginValidationSchema().load(data)
    user = auth_manager.authenticate_user_by_name(data['username'], data['password'])
    from data.users.schemas import UserSchema

    return jwt_manager.login_with_cookies(user.id_user, UserSchema().dump(user)), HTTPStatus.OK

@auth_blueprint.post(f'/{NAME}/login/discord')
async def login_discord():
    data = request.get_json()
    username = data.get('username', None)
    try:
        user: UserModel = user_registry.get_one_or_fail_where(username=username)
    except BaseCustomError:
        raise UnauthorizedError
    id_user = str(user.id_user)
    bot.user_in_auth.append(id_user)
    bot.send_direct_message(f"Bonjour {user.username} veuillez approuver la connexion, si ce n'est pas vous qui avez demandé à vous connecter, veuillez ignorer ce message",
                                  user.id_discord,
                                  buttons=[Button(label="Approuver", style=ButtonStyle.success, custom_id=f'auth_discord_{id_user}')])
    for i in range(20):
        if id_user not in bot.user_in_auth:
            from data.users.schemas import UserSchema
            return jwt_manager.login_with_cookies(user.id_user, UserSchema().dump(user)), HTTPStatus.OK
        sleep(1)
    bot.user_in_auth.remove(id_user)
    raise UnauthorizedError



@auth_blueprint.get(f'/{NAME}/logout')
@jwt_required()
def logout():
    return jwt_manager.logout_with_cookies(), HTTPStatus.OK


docs.register_function(login, auth_blueprint)


@auth_blueprint.get(f'/{NAME}/refresh_token')
@jwt_required(refresh=True)
def refresh_token():
    id_user = get_jwt_identity()
    access_token = jwt_manager.generate_token(id_user, is_refresh=True)
    return {'access_token': access_token}, HTTPStatus.OK
