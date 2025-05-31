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
    model="openai/gpt-4o-mini",  # ,"qwen/qwen3-1.7b",#"openai/gpt-4o-mini",
    messages=[{"role": "user", "content": "What's the weather like in Paris today?"}],
    tools=tools,
    stream=True,
)
import pprint

for s in completion:
    print(s)
"""
ChatCompletionChunk(id='chatcmpl-ib7umc0agyl0vwusbisn', choices=[Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None, tool_calls=[ChoiceDeltaToolCall(index=0, id=None, function=ChoiceDeltaToolCallFunction(arguments='"}', name=None), type='function')]), finish_reason=None, index=0, logprobs=None)], created=1748530158, model='qwen/qwen3-1.7b', object='chat.completion.chunk', service_tier=None, system_fingerprint='qwen/qwen3-1.7b', usage=None)
ChatCompletionChunk(id='chatcmpl-ib7umc0agyl0vwusbisn', choices=[Choice(delta=ChoiceDelta(content=None, function_call=None, refusal=None, role=None, tool_calls=None), finish_reason='tool_calls', index=0, logprobs=None)], created=1748530158, model='qwen/qwen3-1.7b', object='chat.completion.chunk', service_tier=None, system_fingerprint='qwen/qwen3-1.7b', usage=None)
"""
