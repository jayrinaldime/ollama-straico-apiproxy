from pydantic import BaseModel
from openai import OpenAI, Client


# Set a custom base URL (optional)

client = Client(base_url="http://127.0.0.1:3214/v1", api_key="api_key")


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    response_format=CalendarEvent,
)

event = completion.choices[0].message.parsed
print(event)
import pprint

pprint.pprint(completion.model_dump())
"""
{'choices': [{'finish_reason': 'stop',
              'index': 0,
              'logprobs': None,
              'message': {'audio': None,
                          'content': '{"name":"Science '
                                     'Fair","date":"Friday","participants":["Alice","Bob"]}',
                          'function_call': None,
                          'parsed': {'date': 'Friday',
                                     'name': 'Science Fair',
                                     'participants': ['Alice', 'Bob']},
                          'refusal': None,
                          'role': 'assistant',
                          'tool_calls': []}}],
 'created': 1735577217,
 'id': 'chatcmpl-AkDCrMkn5kXjMNnmu6hLwuREnp2NZ',
 'model': 'gpt-4o-mini-2024-07-18',
 'object': 'chat.completion',
 'service_tier': None,
 'system_fingerprint': 'fp_0aa8d3e20b',
 'usage': {'completion_tokens': 18,
           'completion_tokens_details': {'accepted_prediction_tokens': 0,
                                         'audio_tokens': 0,
                                         'reasoning_tokens': 0,
                                         'rejected_prediction_tokens': 0},
           'prompt_tokens': 92,
           'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0},
           'total_tokens': 110}}
"""
