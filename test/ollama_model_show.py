# from ollama import chat
from pydantic import BaseModel
from ollama import Client, AsyncClient

BASE_URL = "http://127.0.0.1:3214"
client = Client(host=BASE_URL)
chat = client.chat
MODEL = "anthropic/claude-3.7-sonnet"

details = client.show(model=MODEL)

print(details.capabilities)
