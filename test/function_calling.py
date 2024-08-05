import json
import ollama
import asyncio

BASE_URL = "http://127.0.0.1:3214"

MODEL = "openai/gpt-4o-mini"


# Simulates an API call to get flight times
# In a real application, this would fetch data from a live database or API
def get_flight_times(departure: str, arrival: str) -> str:
    flights = {
        "NYC-LAX": {
            "departure": "08:00 AM",
            "arrival": "11:30 AM",
            "duration": "5h 30m",
        },
        "LAX-NYC": {
            "departure": "02:00 PM",
            "arrival": "10:30 PM",
            "duration": "5h 30m",
        },
        "LHR-JFK": {
            "departure": "10:00 AM",
            "arrival": "01:00 PM",
            "duration": "8h 00m",
        },
        "JFK-LHR": {
            "departure": "09:00 PM",
            "arrival": "09:00 AM",
            "duration": "7h 00m",
        },
        "CDG-DXB": {
            "departure": "11:00 AM",
            "arrival": "08:00 PM",
            "duration": "6h 00m",
        },
        "DXB-CDG": {
            "departure": "03:00 AM",
            "arrival": "07:30 AM",
            "duration": "7h 30m",
        },
    }

    key = f"{departure}-{arrival}".upper()
    return json.dumps(flights.get(key, {"error": "Flight not found"}))


async def streaming_run(model: str = MODEL):
    client = ollama.AsyncClient(host=BASE_URL)
    # Initialize conversation with a user query
    messages = [
        {
            "role": "user",
            "content": "What is the flight time from New York (NYC) to Los Angeles (LAX)?",
        }
    ]

    # First API call: Send the query and function description to the model
    request = client.chat(
        model=model,
        stream=True,
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_flight_times",
                    "description": "Get the flight times between two cities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "departure": {
                                "type": "string",
                                "description": "The departure city (airport code)",
                            },
                            "arrival": {
                                "type": "string",
                                "description": "The arrival city (airport code)",
                            },
                        },
                        "required": ["departure", "arrival"],
                    },
                },
            },
        ],
    )
    parts = []
    tools = []
    async for part in await request:
        parts.append(part["message"]["content"])
        tools.append(part["message"]["tool_calls"])
        assert part["model"] == MODEL
    whole = " ".join(parts)
    actual_text = whole.strip()
    # Add the model's response to the conversation history
    messages.append(whole)
    response = {}
    # Check if the model decided to use the provided function
    if not response["message"].get("tool_calls"):
        print("The model didn't use the function. Its response was:")
        print(response["message"]["content"])
        return

    # Process function calls made by the model
    if response["message"].get("tool_calls"):
        available_functions = {
            "get_flight_times": get_flight_times,
        }
        for tool in response["message"]["tool_calls"]:
            function_to_call = available_functions[tool["function"]["name"]]
            function_response = function_to_call(
                tool["function"]["arguments"]["departure"],
                tool["function"]["arguments"]["arrival"],
            )
            # Add function response to the conversation
            messages.append(
                {
                    "role": "tool",
                    "content": function_response,
                }
            )

    # Second API call: Get final response from the model
    final_response = await client.chat(model=model, messages=messages)
    print(final_response["message"]["content"])


async def run(model: str = MODEL):
    client = ollama.AsyncClient(host=BASE_URL)
    # Initialize conversation with a user query
    messages = [
        {
            "role": "user",
            "content": "What is the flight time from New York (NYC) to Los Angeles (LAX)?",
        }
    ]

    # First API call: Send the query and function description to the model
    response = await client.chat(
        model=model,
        messages=messages,
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_flight_times",
                    "description": "Get the flight times between two cities",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "departure": {
                                "type": "string",
                                "description": "The departure city (airport code)",
                            },
                            "arrival": {
                                "type": "string",
                                "description": "The arrival city (airport code)",
                            },
                        },
                        "required": ["departure", "arrival"],
                    },
                },
            },
        ],
    )

    # Add the model's response to the conversation history
    messages.append(response["message"])

    # Check if the model decided to use the provided function
    if not response["message"].get("tool_calls"):
        print("The model didn't use the function. Its response was:")
        print(response["message"]["content"])
        return

    # Process function calls made by the model
    if response["message"].get("tool_calls"):
        available_functions = {
            "get_flight_times": get_flight_times,
        }
        for tool in response["message"]["tool_calls"]:
            function_to_call = available_functions[tool["function"]["name"]]
            function_response = function_to_call(
                tool["function"]["arguments"]["departure"],
                tool["function"]["arguments"]["arrival"],
            )
            # Add function response to the conversation
            messages.append(
                {
                    "role": "tool",
                    "content": function_response,
                }
            )

    # Second API call: Get final response from the model
    final_response = await client.chat(model=model, messages=messages)
    print(final_response["message"]["content"])


async def itermodels():
    client = ollama.AsyncClient(host=BASE_URL)
    models = await client.list()

    for model in models["models"]:
        model_name = model["model"]
        print("------------------------------")
        print("Testing model", model_name)
        try:
            await run(model_name)
        except:
            print("failed")
        print("\n")


# Run the async function

if __name__ == "__main__1":
    asyncio.run(itermodels())

if __name__ == "__main__":
    asyncio.run(run("perplexity/llama-3-sonar-small-32k-online"))

if __name__ == "__main__1":
    asyncio.run(streaming_run("openai/gpt-4o-mini:latest"))
