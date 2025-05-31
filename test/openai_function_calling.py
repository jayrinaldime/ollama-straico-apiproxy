from openai import OpenAI, Client

# Set your OpenAI API key
api_key = "skkkkkk"

# Set a custom base URL (optional)

client = Client(base_url="http://127.0.0.1:3214/v1", api_key=api_key)
# Define the conversation

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "parameters": {
                "type": "object",
                "properties": {"location": {"type": "string"}},
            },
        },
    }
]

completion = client.chat.completions.create(
    model="openai/gpt-4o-mini",#"qwen/qwen3-1.7b",#"openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "What's the weather like in Paris today?"}],
    tools=tools,
    stream=False
)
import pprint
pprint.pprint(completion.model_dump())
"""
{'choices': [{'finish_reason': 'tool_calls',
              'index': 0,
              'logprobs': None,
              'message': {'audio': None,
                          'content': None,
                          'function_call': None,
                          'refusal': None,
                          'role': 'assistant',
                          'tool_calls': [{'function': {'arguments': '{"location":"Paris"}',
                                                       'name': 'get_weather'},
                                          'id': 'call_FdTNBSeC9RIzk2xOOgx9C0Ty',
                                          'type': 'function'}]}}],
                                          
                                          
 'created': 1735577518,
 'id': 'chatcmpl-AkDHicpR1N8hsMO5HbdNyTMdtOZ5w',
 'model': 'gpt-4o-2024-08-06',
 'object': 'chat.completion',
 'service_tier': None,
 'system_fingerprint': 'fp_5f20662549',
 'usage': {'completion_tokens': 15,
           'completion_tokens_details': {'accepted_prediction_tokens': 0,
                                         'audio_tokens': 0,
                                         'reasoning_tokens': 0,
                                         'rejected_prediction_tokens': 0},
           'prompt_tokens': 45,
           'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0},
           'total_tokens': 60}}
           
[ChatCompletionMessageToolCall(id='725518481', function=Function(arguments='{"location":"Paris"}', name='get_weather'), type='function')]
[ChatCompletionMessageToolCall(id='fc_150113076', function=None, type='function_call', name='get_weather', arguments='{"location":"Paris, France"}', call_id='call_150113076')]

"""
print(completion.choices[0].message.tool_calls)


