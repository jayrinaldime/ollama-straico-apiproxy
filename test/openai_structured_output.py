from pydantic import BaseModel
from openai import OpenAI, Client
# Set your OpenAI API key
api_key = "skkkkkk"

# Set a custom base URL (optional)

client = Client(base_url="http://127.0.0.1:3214/v1", api_key=api_key)

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

completion = client.beta.chat.completions.parse(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed