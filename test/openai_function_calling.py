import openai
from datetime import datetime
import json

# Simulate the order_id and delivery_date
order_id = "order_12345"
delivery_date = datetime.now()

# Simulate the tool call response
response = {
    "choices": [
        {
            "message": {
                "role": "assistant",
                "tool_calls": [
                    {
                        "id": "call_62136354",
                        "type": "function",
                        "function": {
                            "arguments": "{'order_id': 'order_12345'}",
                            "name": "get_delivery_date",
                        },
                    }
                ],
            }
        }
    ]
}

# Create a message containing the result of the function call
function_call_result_message = {
    "role": "tool",
    "content": json.dumps(
        {
            "order_id": order_id,
            "delivery_date": delivery_date.strftime("%Y-%m-%d %H:%M:%S"),
        }
    ),
    "tool_call_id": response["choices"][0]["message"]["tool_calls"][0]["id"],
}

# Prepare the chat completion call payload
completion_payload = {
    "model": "gpt-4o",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful customer support assistant. Use the supplied tools to assist the user.",
        },
        {
            "role": "user",
            "content": "Hi, can you tell me the delivery date for my order?",
        },
        {
            "role": "assistant",
            "content": "Hi there! I can help with that. Can you please provide your order ID?",
        },
        {"role": "user", "content": "i think it is order_12345"},
        response["choices"][0]["message"],
        function_call_result_message,
    ],
}

# Call the OpenAI API's chat completions endpoint to send the tool call result back to the model
response = openai.chat.completions.create(
    model=completion_payload["model"], messages=completion_payload["messages"]
)
print(response.json())

# Print the response from the API. In this case it will typically contain a message such as "The delivery date for your order #12345 is xyz. Is there anything else I can help you with?"
print(response)
