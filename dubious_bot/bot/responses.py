import random

def get_response(message: str) -> str:
    p_message = message.lower()

    #match on input message
    if p_message == 'hello':
        return 'aloha'

    