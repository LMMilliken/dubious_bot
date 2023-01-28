from typing import Optional
from dubious_bot.brain.api import complete
from dubious_bot.brain.writer import Prompt, Writer
from dubious_bot.constants import START_SEQUENCE, STOP_SEQUENCE, SUBJECTS_PATH

default_writer = Writer.from_posts(SUBJECTS_PATH + 'persona1_posts.txt')

def ask(
    prompt: str,
    writer: Optional[Writer] = None,
    temperature: float = 0.8,
    max_tokens: int = 200,
    top_p = 1,
    frequency_penalty=0,
    presence_penalty=0.6,
    stop=[START_SEQUENCE, STOP_SEQUENCE],
    ):
    if not writer:
        writer = default_writer
    res = complete(
        prompt=prompt,
        writer=writer,
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
        stop=stop,
    )
    return res
    
