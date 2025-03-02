from http import HTTPStatus

from flask import Blueprint, request
from setup import bot

from managers.discord_manager.discord_manager import DiscordManager
from utils.request_default_responses import DefaultResponse

NAME = 'discord'

discord_blueprint = Blueprint(f'{NAME}_blueprint', __name__)


@discord_blueprint.post(f'/{NAME}/send_message')
async def send_message():
    data = request.get_json()
    if 'content' not in data or 'channel_id' not in data:
        return DefaultResponse.error('channel_id and content are required'), HTTPStatus.BAD_REQUEST

    content = data['content']
    channel_id = data['channel_id']
    bot.send_message(content, channel_id)
    return DefaultResponse.success('Message sent'), HTTPStatus.OK
