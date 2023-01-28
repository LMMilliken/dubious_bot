import os
import openai

with open('credentials/openai_key.txt', 'r') as f:
    openai.api_key = f.read()