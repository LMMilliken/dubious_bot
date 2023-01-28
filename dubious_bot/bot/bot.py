import discord
from dubious_bot.brain.writer import Writer
from dubious_bot.constants import DEFAULT_PERSONA
import responses
# ip8rSKVtxRb3tzj

async def send_message(message, user_message):
    try:

        response = responses.get_response(user_message)
        await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    with open('credentials/bot_token.txt', 'r') as f:
        token = f.read()

    intents = discord.Intents.default()

    intents.message_content = True

    client = discord.Client(intents=intents)

    writer = Writer.from_json(DEFAULT_PERSONA)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        print(f'Using persona: {writer.name}')



    @client.event
    async def on_message(message):
        if message.author != client.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)
