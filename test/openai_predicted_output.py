from openai import OpenAI, Client

code = """
class User {
  firstName: string = "";
  lastName: string = "";
  username: string = "";
}

export default User;
"""

refactor_prompt = """
Replace the "username" property with an "email" property. Respond only 
with code, and with no markdown formatting.
"""

api_key = "skkkkkk"

# Set a custom base URL (optional)

client = Client(base_url="http://127.0.0.1:3214/v1", api_key=api_key)

completion = client.chat.completions.create(
    model="openai/gpt-4o-mini",
    messages=[
        {"role": "user", "content": refactor_prompt},
        {"role": "user", "content": code},
    ],
    prediction={"type": "content", "content": code},
)


print(completion.choices[0].message.content)
# import pprint
# pprint.pprint(completion.model_dump())
"""{'choices': [{'finish_reason': 'stop',
              'index': 0,
              'logprobs': None,
              'message': {'audio': None,
                          'content': '\n'
                                     'class User {\n'
                                     '  firstName: string = "";\n'
                                     '  lastName: string = "";\n'
                                     '  email: string = "";\n'
                                     '}\n'
                                     '\n'
                                     'export default User;',
                          'function_call': None,
                          'refusal': None,
                          'role': 'assistant',
                          'tool_calls': None}}],
 'created': 1735577431,
 'id': 'chatcmpl-AkDGJGmJlxXDwNjtVuw4JWae85BGZ',
 'model': 'gpt-4o-2024-08-06',
 'object': 'chat.completion',
 'service_tier': None,
 'system_fingerprint': 'fp_5f20662549',
 'usage': {'completion_tokens': 40,
           'completion_tokens_details': {'accepted_prediction_tokens': 19,
                                         'audio_tokens': 0,
                                         'reasoning_tokens': 0,
                                         'rejected_prediction_tokens': 10},
           'prompt_tokens': 66,
           'prompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0},
           'total_tokens': 106}}
"""
