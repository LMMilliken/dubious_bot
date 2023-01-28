import os

import openai
from writer import Prompt, Writer

from dubious_bot.constants import START_SEQUENCE, STOP_SEQUENCE

with open("credentials/openai_key.txt", "r") as f:
    openai.api_key = f.read()

start_sequence = "\n" + START_SEQUENCE
restart_sequence = "\n" + STOP_SEQUENCE + " "


def ask(prompt: str, writer: Writer, **kwargs):
    prompt = Prompt(prompt)

    full_prompt = writer.make_prompt(prompt)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=full_prompt,
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[START_SEQUENCE, STOP_SEQUENCE],
    )

    print(response)
    return response
