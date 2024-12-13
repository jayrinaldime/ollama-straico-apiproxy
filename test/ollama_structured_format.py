# from ollama import chat
from pydantic import BaseModel
from ollama import Client, AsyncClient


class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]


BASE_URL = "http://127.0.0.1:3214"
client = Client(host=BASE_URL)
chat = client.chat
MODEL = "openai/gpt-4o-mini"  #'qwen2.5:0.5b' #
response = chat(
    messages=[
        {
            "role": "user",
            "content": "Tell me about Japan.",
        }
    ],
    model=MODEL,
    format=Country.model_json_schema(),
    # stream=True
)
# parts=[]
# tools=[]
# for part in response:
#   parts.append(part)
# tools.append(part["message"]["tool_calls"])
# assert part["model"] == MODEL
country = Country.model_validate_json(response.message.content)
print(country)
