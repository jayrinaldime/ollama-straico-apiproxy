# from ollama import chat
from pydantic import BaseModel
from ollama import Client, AsyncClient


BASE_URL = "http://127.0.0.1:3214"
client = Client(host=BASE_URL)

values = client.embeddings(
  model='nomic-ai/nomic-embed-text-v1.5',
  prompt='This is a test',
)

print(values)