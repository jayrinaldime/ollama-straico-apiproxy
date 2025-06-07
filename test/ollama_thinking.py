import pytest
from ollama import Client, AsyncClient

BASE_URL = "http://127.0.0.1:3214"
MODEL = "google/gemini-2.5-flash-preview:thinking"
MSGS = [
    {
        "role": "user",
        "content": "What is 10 + 23?",
    },
]

client = Client(host=BASE_URL)
response = client.chat(model=MODEL, messages=MSGS, think=False)

print(f"Thinking:\n========\n\n {response.message.thinking}")
print("\nResponse:\n========\n\n" + response.message.content)


response = client.chat(model=MODEL, messages=MSGS, think=True)

print(f"Thinking:\n========\n\n {response.message.thinking}")
print("\nResponse:\n========\n\n" + response.message.content)

response = client.chat(model=MODEL, messages=MSGS)

print(f"Thinking:\n========\n\n {response.message.thinking}")
print("\nResponse:\n========\n\n" + response.message.content)
