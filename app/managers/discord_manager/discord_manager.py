import asyncio
import json
import requests
from functools import wraps
from collections.abc import Sequence

import discord
from discord import Member, Role, app_commands
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
        self.token = token
        self.logger = get_console_logger('bot_manager')

        intents = discord.Intents.all()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.tree = app_commands.CommandTree(self.client)

        self.client.event(self.on_ready)
        self.client.event(self.on_message)
        self.client.event(self.on_interaction)

        self.user_in_auth = []

    async def on_ready(self):
        self.tree.clear_commands(guild=None)
        self.tree.add_command(self.players)
        await self.tree.sync()
        self.logger.info(f'Commandes synchronisées pour {self.client.user}')

    async def on_interaction(self, interaction: discord.Interaction):
        custom_id = interaction.data.get('custom_id')
        if custom_id and custom_id.startswith('auth_discord_'):
            id_user = custom_id.replace('auth_discord_', '')
            if id_user in self.user_in_auth:
                self.user_in_auth.remove(id_user)
                await interaction.response.edit_message(content='Connexion approuvée', view=None)

    def run(self):
        self.client.run(self.token)

    @app_commands.command(name="players", description="Affiche le nombre de joueurs sur le serveur")
    async def players(self, interaction: discord.Interaction):
        try:
            response = requests.get("http://lyon.mediapi.org:5001/players")
            response.raise_for_status()
            data = response.json()
            await interaction.response.send_message(f"Il y a {data.get('players', 0)} joueurs sur le serveur.")
        except requests.RequestException as e:
            self.logger.error(f"Erreur API: {e}")
            await interaction.response.send_message("Impossible de récupérer les joueurs.", ephemeral=True)

    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.channel.id == 1342417055386960004:
            payload = {"author": str(message.author.display_name), "message": message.content}
            try:
                response = requests.post("http://lyon.mediapi.org:5001/chat", json=payload)
                response.raise_for_status()
            except requests.RequestException as e:
                self.logger.error(f"Erreur API: {e}")
                await message.channel.send("Erreur lors de l'envoi du message à l'API.")

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    @_run_async()
    async def send_message(self, message: str, id_channel: int, *, buttons: list[Button] = None):
        channel = self.client.get_channel(int(id_channel))
        if channel:
            view = View()
            for button in buttons or []:
                view.add_item(button)
            await channel.send(message, view=view)
        else:
            self.logger.error(f'Channel {id_channel} not found.')

    @_run_async()
    async def send_direct_message(self, message: str, id_user: int, *, buttons: list[Button] = None):
        user = await self.client.fetch_user(id_user)
        if user:
            view = View()
            for button in buttons or []:
                view.add_item(button)
            await user.send(message, view=view)
        else:
            self.logger.error(f'User {id_user} not found.')

    async def get_members_from_guild(self, server_id) -> Sequence[Member]:
        server = self.client.get_guild(int(server_id))
        return server.members if server else []

    async def get_roles_from_member(self, server_id, id_member) -> Sequence[Role]:
        server = self.client.get_guild(int(server_id))
        member = server.get_member(int(id_member)) if server else None
        return member.roles if member else []

    @_run_async()
    async def create_role(self, server_id, name, hex_color):
        server = self.client.get_guild(int(server_id))
        if server:
            return await server.create_role(name=name, color=discord.Color(int(hex_color, 16)))
        self.logger.error(f'Server {server_id} not found.')

    @_run_async()
    async def add_role_to_member(self, server_id, id_member, id_role):
        server = self.client.get_guild(int(server_id))
        member, role = server.get_member(int(id_member)), server.get_role(int(id_role)) if server else (None, None)
        if member and role:
            await member.add_roles(role)
        else:
            self.logger.error(f'Member or role not found in server {server_id}.')

    @_run_async()
    async def change_presence(self, activity: str):
        await self.client.change_presence(activity=discord.Game(name=activity))
