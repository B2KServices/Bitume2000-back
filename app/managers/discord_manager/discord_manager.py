from collections.abc import Sequence

import discord
import asyncio
from functools import wraps

from discord import Member

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

    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    async def on_message(self, message):
        print('Message received!')
        if message.author == self.client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    @_run_async()
    async def send_message(self, message, id_channel: int | str):
        channel = self.client.get_channel(int(id_channel))
        if channel:
            await channel.send(message)
        else:
            self.logger.error(f"Channel {id_channel} not found.")

    async def get_members_from_guild(self, server_id) -> Sequence[Member]:
        server = self.client.get_guild(server_id)
        self.logger.debug(server)
        members = server.members
        self.logger.debug(members)
        return members



    def run(self):
        self.client.run(self.token)
