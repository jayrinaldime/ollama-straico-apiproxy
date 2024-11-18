import pytest
from ollama import Client, AsyncClient

BASE_URL = "http://127.0.0.1:3214"
MODEL = "openai/gpt-4o-mini"
MSGS = [
    {
        "role": "user",
        "content": "Tell me a joke",
    },
]

client = Client(host=BASE_URL)
response = client.chat(model=MODEL, messages=MSGS, options={"temperature": 2})
print(response)


response = client.generate(
    model=MODEL, prompt=MSGS[0]["content"], options={"temperature": 2}
)
print(response)
