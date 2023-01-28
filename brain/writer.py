
from datetime import datetime
import os
from typing import Optional, Union
import json

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
        question: str,
        answer: Optional[str] = None,
        time: Optional[datetime] = None,
        must_include: bool = False,
        start: str = 'SUBJECT: ',
        stop: str = 'THECORD: '
        ):
        self.question = question
        self.answer = answer
        self.time = time or datetime.now()
        self.must_include = must_include
        self.start = start
        self.stop = stop

    def __str__(self):
        ret = self.stop + self.question 
        if self.answer:
            ret += '\n' + self.start + self.answer
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

    preamble: str
    logs: list[Prompt]
    memory: int

    def __init__(
        self,
        preamble: Optional[Union[str, int]] = None,
        logs: Optional[list[Prompt]] = None,
        memory: int = -1
    ):
        if isinstance(preamble, str):
            self.preamble = preamble
        else:
            preamble_num = preamble or 0
            current_dir = os.path.dirname(os.path.abspath(__file__))
            fname = current_dir + 'preambles.txt'
            with open(fname, 'r') as f:
                preambles = f.read().split('PREAMBLE!!!BREAK')
                self.preamble = preambles[preamble_num]
    
        self.logs = logs or []
        self.memory = memory

    def __dict__(self):
        return {
            'preamble': self.preamble,
            'memory': self.memory,
            'logs': [dict(log) for log in self.logs]
        }

    def make_prompt(self, next_prompt: Prompt) -> str:
        ret = self.preamble
        ret += '\n'.join([
            str(prompt)
            for prompt in self.logs
            if prompt.must_include  or self.memory < 0 or (
                datetime.now() - prompt.time
                )  < self.memory
        ])
        ret += '\n' + str(next_prompt)
        self.logs.append(next_prompt)
        return ret

    def dump_logs(self, fname: Optional[str] = None):
        json_data = json.dumps(dict(self))
        if fname:
            with open(fname, 'w') as f:
                json.dump(json_data, f)

        return json_data

    @staticmethod
    def from_json(fname: str):
        with open(fname, 'r') as f:
            data = json.load(f)
        
        writer = Writer(
            preamble=data['preamble'],
            logs = [
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
            memory=data['memory']
        )
        return writer
