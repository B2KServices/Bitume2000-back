from http import HTTPStatus

from discord import Interaction, ButtonStyle
from discord.ui import Button

from data.authentication.schemas import LoginValidationSchema
from data.users.models import UserModel
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from managers.authentication_manager import JWTGenerationManager, PasswordAuthManager
from managers.swagger_manager.doc_decorator import swagger
from setup import docs, bot
from utils.registry import SQLAlchemyRegistry
from utils.request_default_responses import DefaultResponse

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
    async def approve_connection(interaction: Interaction):
        await interaction.message.edit('la connexion a ete approuvee')
        return True
    data = request.get_json()
    username = data['username']
    user: UserModel = user_registry.get_one_or_fail_where(username=username)
    approve_button = Button(label="Approuver", style=ButtonStyle.primary)
    buttons = [(approve_button, approve_connection)]
    if await bot.send_direct_message(f"Bonjour {user.username} veuillez approuver la connexion, si ce n'est pas vous qui avez demandé à vous connecter, veuillez ignorer ce message", user.id_discord, buttons=buttons):
        return DefaultResponse.success('La reponse a ete approuvee'), 200




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
