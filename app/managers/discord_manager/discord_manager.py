import discord

class DiscordManager:
    def __init__(self, token):
        intents = discord.Intents.all()
        intents.message_content = True
        self.client = discord.Client(intents=intents)
        self.token = token

        self.client.event(self.on_ready)
        self.client.event(self.on_message)

    async def on_ready(self):
        print(f'We have logged in as {self.client.user}')

    async def on_message(self, message):
        print('Message received!')
        if message.author == self.client.user:
            return

        if message.content.startswith('$hello'):
            await message.channel.send('Hello!')

    async def send_message(self, message):
        id_channel = '1229694215798390881'
        channel = self.client.get_channel(int(id_channel))  # Convertir l'ID en int
        if channel:
            await channel.send(message)
        else:
            print(f"Channel {id_channel} not found.")

    def run(self):
        self.client.run(self.token)
