import discord

class DiscordManager:
    def __init__(self, token):
        intents = discord.Intents.all()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.token = token

    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    async def on_message(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    def run(self):
        self.client.run(self.token)
