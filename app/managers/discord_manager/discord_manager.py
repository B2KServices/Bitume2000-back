import asyncio
import json
import requests
from collections.abc import Sequence
from functools import wraps

import discord
from discord import Member, Role
from discord.ui import Button, View
from utils.console_logger import get_console_logger


def _run_async():
    """
    A decorator to run a coroutine in the Discord event loop and return its result.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self = args[0]  # Assuming the first argument is `self`
            coroutine = func(*args, **kwargs)
            future = asyncio.run_coroutine_threadsafe(coroutine, self.client.loop)
            try:
                return future.result()
            except Exception as e:
                raise RuntimeError(f"Error executing coroutine {func.__name__}: {e}")
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
        self.logger = get_console_logger('bot_manager')

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

        if message.channel.id == 1342417055386960004:
            # Envoi du message à l'API externe
            payload = {
                "author": str(message.author),
                "message": message.content
            }
            try:
                response = requests.post("http://lyon.mediapi.org:5001/chat", json=payload)
                if response.status_code == 200:
                    await message.channel.send("Message envoyé à l'API avec succès!")
                else:
                    await message.channel.send(f"Erreur API: {response.status_code}")
            except requests.RequestException as e:
                self.logger.error(f"Erreur lors de l'envoi du message à l'API: {e}")
                await message.channel.send("Erreur lors de l'envoi du message à l'API.")

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    @_run_async()
    async def send_message(self, message: str, id_channel: int | str, *, buttons: list[Button] | None = None):
        buttons = buttons if buttons else []
        channel = self.client.get_channel(int(id_channel))
        if channel:
            view = View()

            for button in buttons:
                view.add_item(button)

            await channel.send(message, view=view)
        else:
            self.logger.error(f'Channel {id_channel} not found.')

    @_run_async()
    async def send_direct_message(self, message: str, id_user: int | str, *, buttons: list[Button]):
        user = await self.client.fetch_user(id_user)
        if user:
            view = View()
            for button in buttons:
                view.add_item(button)

            await user.send(message, view=view)
        else:
            self.logger.error(f'User {id_user} not found.')

    async def get_members_from_guild(self, server_id) -> Sequence[Member]:
        server = self.client.get_guild(int(server_id))
        return server.members if server else []

    async def get_role_from_guild(self, server_id) -> Sequence[Role]:
        server = self.client.get_guild(int(server_id))
        return server.roles if server else []

    async def get_roles_from_member(self, server_id, id_member) -> Sequence[Role]:
        server = self.client.get_guild(int(server_id))
        if server is None:
            self.logger.error(f'Server with ID {server_id} not found')
            return []

        member = server.get_member(int(id_member))
        if member is None:
            self.logger.error(f'Member with ID {id_member} not found in server {server_id}')
            return []

        return member.roles

    async def get_categorie_from_guild(self, id_server, id_category):
        server = self.client.get_guild(int(id_server))
        if server:
            return discord.utils.get(server.categories, id=int(id_category))
        return None

    @_run_async()
    async def create_role(self, server_id, name, hex_color):
        server = self.client.get_guild(int(server_id))
        if server:
            role = await server.create_role(name=name, color=discord.Color(int(hex_color, 16)))
            return role
        self.logger.error(f'Server {server_id} not found.')

    @_run_async()
    async def add_role_to_member(self, server_id, id_member, id_role):
        server = self.client.get_guild(int(server_id))
        if server:
            member = server.get_member(int(id_member))
            role = server.get_role(int(id_role))
            if member and role:
                await member.add_roles(role)
            else:
                self.logger.error(f'Member or role not found in server {server_id}.')

    @_run_async()
    async def remove_role_from_member(self, server_id, id_member, id_role):
        server = self.client.get_guild(int(server_id))
        if server:
            member = server.get_member(int(id_member))
            role = server.get_role(int(id_role))
            if member and role:
                await member.remove_roles(role)
            else:
                self.logger.error(f'Member or role not found in server {server_id}.')

    @_run_async()
    async def set_channel_on_category(self, server_id, channel_id, id_category):
        server = self.client.get_guild(int(server_id))
        if server:
            channel = server.get_channel(int(channel_id))
            category = await self.get_categorie_from_guild(server_id, id_category)
            if channel and category:
                await channel.edit(category=category)
            else:
                self.logger.error(f'Channel or category not found in server {server_id}.')

    @_run_async()
    async def change_presence(self, activity):
        await self.client.change_presence(activity=discord.Game(name=activity))
