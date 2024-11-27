import json
from app import app, logging
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from backend import prompt_completion

logger = logging.getLogger(__name__)
MODEL_SIZE = 7365960935

from .response.stream.completion_response import generate_ollama_stream, response_stream


@app.post("/api/generate")
async def ollamagenerate(request: Request):
    try:
        msg = await request.json()
    except:
        msg = json.loads((await request.body()).decode())

    logger.debug(msg)
    request_msg = msg["prompt"]
    model = msg.get("model")

    settings = {}
    if "options" in msg:
        options = msg["options"]
        settings["temperature"] = options.get("temperature")
        settings["max_tokens"] = options.get("max_tokens")

    if msg.get("stream") == False:
        response = await prompt_completion(msg["prompt"], model=model, **settings)
        return JSONResponse(
            content={
                "model": model,
                "created_at": "2023-08-04T19:22:45.499127Z",
                "response": response,
                "done": True,
                "total_duration": 10706818083,
                "load_duration": 6338219291,
                "prompt_eval_count": 26,
                "prompt_eval_duration": 130079000,
                "eval_count": 259,
                "eval_duration": 4232710000,
            }
        )

    return StreamingResponse(
        generate_ollama_stream(request_msg, model), media_type="application/x-ndjson"
    )


@app.post("/api/chat")
async def ollamachat(request: Request):
    try:
        msg = await request.json()
    except:
        msg = json.loads((await request.body()).decode())

    model = msg["model"]
    tools = msg.get("tools")
    messages = msg["messages"]

    settings = {}
    if "options" in msg:
        options = msg["options"]
        settings["temperature"] = options.get("temperature")
        settings["max_tokens"] = options.get("max_tokens")

    if tools and len(tools) != 0:
        parent_tool = [
            {
                "role": "system",
                "tools": tools,
                "content": """
If you need to use a tool to answer please use the defined tools. 
Assuming the function is 
```
{"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather for a location","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The location to get the weather for, e.g. San Francisco, CA"},"format":{"type":"string","description":"The format to return the weather in, e.g. 'celsius' or 'fahrenheit'","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
```
When you do use a function your output should like
``` 
{"tool_calls":[{"function":{"name":"get_current_weather","arguments":{"format":"celsius","location":"Paris, FR"}}}]}
``` 
You must answer by exactly following the provided instructions. Do not add any additional comments or explanations.
Do not add "Here is..." or anything like that.

Act like a script, you are given an optional input and the instructions to perform, you answer with the output of the requested task.

Please only output plain json.
                    """.strip(),
            }
        ]
        messages = parent_tool + messages

    if "stream" in msg:
        streaming = msg.get("stream")
    else:
        streaming = True

    logger.debug(msg)
    logger.debug(model)
    images = None
    if type(messages) == list and len(messages) >= 1 and type(messages[0]) == dict:
        images = []
        new_messages = []
        for message in messages:
            if "images" in message:
                img = message["images"]
                if len(img) > 0:
                    images += img
                del message["images"]
            new_messages.append(message)
        messages = new_messages

    request_msg = json.dumps(messages, indent=True, ensure_ascii=False)
    response = await prompt_completion(request_msg, images, model, **settings)
    try:
        response = json.loads(response)
        response_type = type(response)
        if response_type == dict and "content" in response:
            response = response["content"]
        elif (
            response_type == list
            and len(response) > 0
            and type(response[0]) == dict
            and "content" in response[0]
        ):
            response = response[0]["content"]
    except:
        pass
    response_type = type(response)

    original_response = response
    if tools is not None and len(tools) != 0:

        if response_type == str:
            response = response.strip()
            if response.startswith("```json") and response.endswith("```"):
                response = response[7:-3].strip()
                response = json.loads(response)
            elif response.startswith("```") and response.endswith("```"):
                response = response[3:-3].strip()
                response = json.loads(response)
            else:
                try:
                    response = json.loads(response)
                except:
                    pass
        if type(response) == list and len(response) > 0:
            response = response[0]

        if type(response) == dict and "tool_calls" in response:
            return JSONResponse(
                content={
                    "model": model,
                    "created_at": "2024-07-22T20:33:28.123648Z",
                    "message": {
                        "role": "assistant",
                        "content": "",
                        "tool_calls": response["tool_calls"],
                    },
                    "done_reason": "stop",
                    "done": True,
                    "total_duration": 885095291,
                    "load_duration": 3753500,
                    "prompt_eval_count": 122,
                    "prompt_eval_duration": 328493000,
                    "eval_count": 33,
                    "eval_duration": 552222000,
                }
            )

    if len(messages) > 1 and response_type == str:
        response = response.strip()
        if response.startswith("```json") and response.endswith("```"):
            response = response[7:-3].strip()
            original_response = json.loads(response)
        elif response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
            original_response = json.loads(response)
        else:
            try:
                original_response = json.loads(response)

            except:
                pass

            if (
                type(original_response) == dict
                and "role" in original_response
                and original_response["role"] == "assistant"
                and "content" in original_response
            ):
                original_response = original_response["content"]

    if type(original_response) in [dict, list]:
        original_response = json.dumps(original_response)

    if streaming:
        return StreamingResponse(
            response_stream(model, original_response, is_tool=False),
            media_type="application/x-ndjson",
        )
    else:
        return JSONResponse(
            content={
                "model": model,
                "created_at": "2023-12-12T14:13:43.416799Z",
                "message": {"role": "assistant", "content": original_response},
                "done": True,
                "total_duration": 5191566416,
                "load_duration": 2154458,
                "prompt_eval_count": 26,
                "prompt_eval_duration": 383809000,
                "eval_count": 298,
                "eval_duration": 4799921000,
            }
        )
