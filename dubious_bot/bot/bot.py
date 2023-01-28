import discord
from dubious_bot.brain.writer import Writer
from dubious_bot.constants import DEFAULT_PERSONA, ROBOT_NAME
import responses
# ip8rSKVtxRb3tzj

async def send_message(message, response):
    try:

        await message.channel.send(response)

    except Exception as e:
        print(e)


def run_discord_bot():
    with open('credentials/bot_token.txt', 'r') as f:
        token = f.read()

    intents = discord.Intents.default()

    intents.message_content = True

    client = discord.Client(intents=intents)

    guild = client.guilds[0]

    writer = Writer.from_json(DEFAULT_PERSONA)

    bot_member = guild.get_member(client.user.id)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running')
        print(f'Using persona: {writer.name}')


        await bot_member.edit(nick=writer.name)


    @client.event
    async def on_message(message):
        if message.author != client.user:
            username = str(message.author)
            user_message = str(message.content)
            channel = str(message.channel)

            if user_message.startswith(f'hey {writer.name}'):
                response = responses.respond_human(user_message, writer)
                await send_message(message, response)
            elif user_message.lower().startswith(f'hey {ROBOT_NAME}'):
                (response, writer) = await responses.respond_robot(user_message, writer)
                await send_message(message, response)
