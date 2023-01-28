from datetime import datetime, timedelta
from typing import Optional

from dubious_bot.brain.api import complete
from dubious_bot.brain.writer import Prompt, Writer
from dubious_bot.constants import DEFAULT_PERSONA, LOGS_PATH, START_SEQUENCE, STOP_SEQUENCE

default_writer = Writer.from_json(DEFAULT_PERSONA)


def ask(
    prompt: str,
    writer: Optional[Writer] = None,
    temperature: float = 0.8,
    max_tokens: int = 200,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=-0.4,
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

    if not writer.last_dump or datetime.now() - writer.last_dump > timedelta(writer.memory):
        writer.dump_logs()
        writer.last_dump = datetime.now()
        
    return res
