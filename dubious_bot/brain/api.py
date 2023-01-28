import os

import openai

from dubious_bot.brain.writer import Prompt, Writer
from dubious_bot.constants import START_SEQUENCE, STOP_SEQUENCE

with open('credentials/openai_key.txt', 'r') as f:
    openai.api_key = f.read()

start_sequence = '\n' + START_SEQUENCE
restart_sequence = '\n' + STOP_SEQUENCE + ' '


def complete(
    prompt: str,
    writer: Writer,
    temperature: float,
    max_tokens: int,
    top_p,
    frequency_penalty,
    presence_penalty,
    stop,
):
    prompt = Prompt(prompt)

    full_prompt = writer.make_prompt(prompt)

    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=full_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
    response_text = response.choices[0].text

    prompt.answer = response_text

    return response_text
