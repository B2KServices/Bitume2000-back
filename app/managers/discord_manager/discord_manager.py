from collections.abc import Sequence

import discord
import asyncio
from functools import wraps

from discord import Member, Role, Interaction, Message, ButtonStyle
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
        self.client.event(self.on_interaction)
        self.user_in_auth = []
        self.logger = get_console_logger(f'bot_manager')

    async def on_interaction(self, interaction: discord.Interaction):
        custom_id = interaction.data.get('custom_id')
        if custom_id and custom_id.startswith('auth_discord_'):
            id_user = custom_id.replace('auth_discord_', '')
            if id_user in self.user_in_auth:
                self.user_in_auth.remove(id_user)
                await interaction.response.edit_message(content='Connexion approuvée', view=None)

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
    async def send_message(self, message: str, id_channel: int | str, *, buttons: list[Button]):
        channel = self.client.get_channel(int(id_channel))
        if channel:
            view = View()

            for button in buttons:
                view.add_item(button)

            await channel.send(message, view=view)
        else:
            self.logger.error(f"Channel {id_channel} not found.")

    @_run_async()
    async def send_direct_message(self, message: str, id_user: int | str, *, buttons: list[Button]):
        user = await self.client.fetch_user(id_user)
        if user:
            view = View()
            for button in buttons:
                view.add_item(button)

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

    async def get_roles_from_member(self, server_id, id_member) -> Sequence[Role]:
        server = self.client.get_guild(int(server_id))
        self.logger.info(f"Server: {server}")

        if server is None:
            self.logger.error(f"Server with ID {server_id} not found")
            return []

        member = server.get_member(int(id_member))
        self.logger.info(f"Member: {member}")

        if member is None:
            self.logger.error(f"Member with ID {id_member} not found in server {server_id}")
            return []

        roles = member.roles
        self.logger.info(f"Roles: {roles}")
        return roles

    @_run_async()
    async def create_role(self, server_id, name, hex_color):
        server = self.client.get_guild(int(server_id))
        role = await server.create_role(name=name, color=discord.Color(int(hex_color, 16)))
        return role

    @_run_async()
    async def add_role_to_member(self, server_id, id_member, id_role):
        server = self.client.get_guild(int(server_id))
        member = server.get_member(int(id_member))
        role = server.get_role(int(id_role))
        await member.add_roles(role)


    @_run_async()
    async def remove_role_from_member(self, server_id, id_member, id_role):
        server = self.client.get_guild(int(server_id))
        member = server.get_member(int(id_member))
        role = server.get_role(int(id_role))
        await member.remove_roles(role)

