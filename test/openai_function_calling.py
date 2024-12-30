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
              "properties": {
                  "location": {"type": "string"}
              },
          },
      },
  }
]

completion = client.chat.completions.create(
  model="gpt-4o",
  messages=[{"role": "user", "content": "What's the weather like in Paris today?"}],
  tools=tools,
)

print(completion.choices[0].message.tool_calls)