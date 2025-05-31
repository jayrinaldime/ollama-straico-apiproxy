def add_two_numbers(a: int, b: int) -> int:
    """
    Add two numbers

    Args:
      a (set): The first number as an int
      b (set): The second number as an int

    Returns:
      int: The sum of the two numbers
    """
    return a + b


from ollama import chat, Client

messages = [{"role": "user", "content": "what is three minus one?"}]
BASE_URL = "http://127.0.0.1:3214"
client = Client(host=BASE_URL)
response = client.chat(
    model="openai/gpt-4o-mini",
    messages=messages,
    tools=[add_two_numbers],  # Python SDK supports passing tools as functions
    stream=True,
)

for chunk in response:
    # Print model content
    print(chunk.message.content, end="", flush=True)
    # Print the tool call
    if chunk.message.tool_calls:
        print(chunk.message.tool_calls)
