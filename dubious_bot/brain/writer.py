import json
import os
from datetime import datetime, timedelta
from typing import Optional, Union

from dubious_bot.constants import POST_BREAK, START_SEQUENCE, STOP_SEQUENCE


class Prompt:
    question: str
    answer: Optional[str]
    time: datetime
    must_include: bool
    start: str
    stop: str
    time_format: str = '%Y-%m-%d %H:%M:%S'

    def __init__(
        self,
        question: Optional[str] = None,
        answer: Optional[str] = None,
        time: Optional[datetime] = None,
        must_include: bool = False,
        start: str = START_SEQUENCE + ' ',
        stop: str = STOP_SEQUENCE + ' ',
    ):
        self.question = question
        self.answer = answer
        self.time = time or datetime.now()
        self.must_include = must_include
        self.start = start
        self.stop = stop

    def __str__(self):
        ret = ''
        if self.question:
            ret += self.stop + self.question
            if self.answer:
                ret += '\n'
        if self.answer:
            ret += self.start + self.answer
        return ret

    def __dict__(self):
        return {
            'question': self.question,
            'answer': self.answer,
            'time': self.time.strftime(self.time_format),
            'must_include': self.must_include,
            'start': self.start,
            'stop': self.stop,
        }


class Writer:

    name: str
    preamble: str
    logs: list[Prompt]
    memory: int

    def __init__(
        self,
        name: str = 'human',
        preamble: Optional[Union[str, int]] = None,
        logs: Optional[list[Prompt]] = None,
        memory: int = -1,
    ):
        if isinstance(preamble, str):
            self.preamble = preamble
        else:
            preamble_num = preamble or 0
            current_dir = os.path.dirname(os.path.abspath(__file__))
            fname = current_dir + '/preambles.txt'
            with open(fname, 'r') as f:
                preambles = f.read().split('\nPREAMBLE!!!BREAK\n')
                self.preamble = preambles[preamble_num]

        self.name = name
        self.logs = logs or []
        self.memory = memory

    def __dict__(self):
        now = datetime.now()
        return {
            'name': self.name,
            'preamble': self.preamble,
            'memory': self.memory,
            'logs': [log.__dict__() for log in self.logs
                if not self.within_memory or
                now - log.time < timedelta(minutes=self.memory)
            ],
        }

    def make_prompt(self, next_prompt: Optional[Prompt] = None) -> str:
        ret = self.preamble + '\n'
        ret += '\n'.join(
            [
                str(prompt)
                for prompt in self.logs
                if prompt.must_include
                or self.memory < 0
                or (datetime.now() - prompt.time) < timedelta(minutes=self.memory)
            ]
        )
        if next_prompt:
            ret += '\n' + str(next_prompt)
            self.logs.append(next_prompt)
        ret += '\n' + START_SEQUENCE + ' '
        return ret

    def remember(self, duration: Optional[int] = None):
        if not duration:
            duration = self.memory
        now = datetime.now()
        for prompt in self.logs:
            if now - prompt < timedelta(minutes=self.memory):
                prompt.must_include = True

    def dump_logs(self, fname: Optional[str] = None, within_memory: bool = False):
        self.within_memory = within_memory
        if fname:
            with open(fname, 'w') as f:
                json.dump(self.__dict__(), f, indent=4)
        
        del self.within_memory

        return self.__dict__()

    @staticmethod
    def from_json(fname: str):
        with open(fname, 'r') as f:
            data = json.load(f)

        writer = Writer(
            preamble=data['preamble'],
            logs=[
                Prompt(
                    question=log['question'],
                    answer=log.get('answer', None),
                    time=datetime.strptime(log['time'], Prompt.format),
                    must_include=log['must_include'],
                    start=log['start'],
                    stop=log['stop'],
                )
                for log in data['logs']
            ],
            memory=data['memory'],
        )
        return writer

    @staticmethod
    def from_posts(
        fname: str,
        name: Optional[str] = None,
        preamble: Optional[Union[str, int]] = None,
        memory: Optional[int] = None,
    ):
        with open(fname, 'r') as f:
            posts = f.read().split(POST_BREAK)
        prompts = [Prompt(answer=post, must_include=True) for post in posts]
        writer = Writer(preamble=preamble, logs=prompts)
        if memory:
            writer.memory = memory
        if name:
            writer.name = name
        return writer
