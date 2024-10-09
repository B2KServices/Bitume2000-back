from collections.abc import Sequence

import discord
import asyncio
from functools import wraps

from discord import Member, Role
from discord.ui import View, Button

from utils.console_logger import get_console_logger


def _run_async():
    """
    A decorator to run a coroutine in the Discord event loop.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]  # Assuming the first argument is `self`
            coroutine = func(*args, **kwargs)
            asyncio.run_coroutine_threadsafe(coroutine, self.client.loop)

        return wrapper

    return decorator

class DiscordManager:

    def __init__(self, token):
        intents = discord.Intents.all()
        intents.message_content = True
        intents.members = True
        intents.presences = True
        self.client = discord.Client(intents=intents)
        self.token = token

        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.logger = get_console_logger(f'{self.client.user}')


    def run(self):
        self.client.run(self.token)

    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    async def on_message(self, message):
        print('Message received!')
        if message.author == self.client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    @_run_async()
    async def send_message(self, message: str, id_channel: int | str, *, buttons: list[tuple[Button, callable]]):
        channel = self.client.get_channel(int(id_channel))
        if channel:
            view = View()

            for button, func in buttons:
                view.add_item(button)

                @button.callback
                async def button_callback(interaction, action=func):
                    await action(interaction)

            await channel.send(message, view=view)
        else:
            self.logger.error(f"Channel {id_channel} not found.")

    @_run_async()
    async def send_direct_message(self, message: str, id_user: int | str, *, buttons: list[tuple[Button, callable]]):
        user = await self.client.fetch_user(id_user)
        if user:
            view = View()

            for button, func in buttons:
                view.add_item(button)

                @button.callback
                async def button_callback(interaction, action=func):
                    result = await action(interaction)
                    return result

            await user.send(message, view=view)
        else:
            self.logger.error(f"User {id_user} not found.")

    async def get_members_from_guild(self, server_id) -> Sequence[Member]:
        server = self.client.get_guild(int(server_id))
        members = server.members
        return members

    async def get_role_from_guild(self, server_id) -> Sequence[Role]:
        server = self.client.get_guild(int(server_id))
        roles = server.roles
        return roles
