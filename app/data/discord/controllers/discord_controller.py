from http import HTTPStatus

from flask import Blueprint, request

from data.users.models import UserModel
from setup import bot

from utils.registry import SQLAlchemyRegistry
from utils.request_default_responses import DefaultResponse

NAME = 'discord'

discord_blueprint = Blueprint(f'{NAME}_blueprint', __name__)
registry_user = SQLAlchemyRegistry(UserModel)


@discord_blueprint.post(f'/{NAME}/send_message')
async def send_message():
    data = request.get_json()
    if 'content' not in data or 'channel_id' not in data:
        return DefaultResponse.error('channel_id and content are required'), HTTPStatus.BAD_REQUEST

    content: str = data['content']
    channel_id = data['channel_id']
    args = content.split(' ')
    i = 0
    for arg in args:
        if arg.startswith('@'):
            possibly_name: str = arg[1:]
            user: list[UserModel] = registry_user.get_all_where(username=possibly_name.lower())
            if len(user) == 1:
                args[i] = f"<@{user[0].id_discord}>"
        i+=1


    bot.send_message(" ".join(args), channel_id)
    return DefaultResponse.success('Message sent'), HTTPStatus.OK
