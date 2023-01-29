from dubious_bot import brain
from dubious_bot.brain.writer import Writer
from dubious_bot.constants import ROBOT_NAME
import random
from discord import Client
from os.path import isfile

def get_response(message: str) -> str:
    p_message = message.lower()

    #match on input message
    if p_message == 'hello':
        return 'aloha'

    

def respond_human(message: str, writer: Writer):
    message = message[len(f'hey {writer.name}') + 1:].strip()
    response = brain.ask(message, writer)
    return response


async def respond_robot(message: str, writer: Writer, client: Client):
    message = message[len(f'hey {ROBOT_NAME}')+1:].strip()
    robot_noises = ['BZZT', 'beep boop', '*whirrrr*']
    response = ''

    if message.lower().startswith('remember that'):
        if '-v' in message:
            duration = int(message.split('-v')[1])
            writer.remember(duration=duration)
        else:
            duration = None
            writer.remember()
        response = (
            'keeping track of all queries made in the last'
            f' {duration or writer.memory} minutes'
            )

    elif message.lower().startswith('rename to '):
        new_name = message[len('rename to'):].strip()
        writer.dump_logs()
        writer.name = new_name
        writer.last_dump = None

        guild = client.guilds[0]
        bot_member = guild.get_member(client.user.id)
        await bot_member.edit(nick=writer.name)

        response = (
            f'I shall be known as {writer.name} henceforth!'
        )

    elif message.lower().startswith('become '):

        page_flag = None
        if ' -page ' in message:
            page_flag = ' -page '
        elif ' -p ' in message:
            page_flag = ' -p '
        else:
            response = (
                'please provide a url for either page to scrape, '
                'or a local posts (.txt) or logs (.json) file using '
                'either the `-p` or `-page` flag'
            )
        
        if page_flag:
        
            name_flag = None
            if ' -name ' in message:
                name_flag = ' -name '
            elif ' -n ' in message:
                name_flag = ' -n '
            if name_flag:
                name = message.split(name_flag)[1].strip().split(' ')[0]
            else:
                name = None
        
            url = message.split(page_flag)[1].strip().split(' ')[0]
            if isfile(url):
                if url.endswith('.json'):
                    writer = Writer.from_json(url)
                elif url.endswith('.txt'):
                    writer = Writer.from_posts(url, name)
            else:
                pass 
                #TODO


    return (random.choice(robot_noises) + ' - ' + response, writer)

