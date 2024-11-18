import openai

# Set your OpenAI API key
api_key = "skkkkkk"

# Set a custom base URL (optional)

client = openai.Client(base_url="http://127.0.0.1:3214", api_key=api_key)
# Define the conversation
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke."},
]


# Make the API call for chat completion
response = client.chat.completions.create(
    model="openai/gpt-4o-mini",  # You can change this to another model if needed
    messages=messages,
    temperature=2.0,  # Set temperature to 2.0 for more randomness
    max_tokens=150,  # Limit the response length
)

# Extract and print the assistant's reply

print("Assistant:", response)
