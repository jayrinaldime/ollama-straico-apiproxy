import json
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from app import app, logging
from backend import prompt_completion

from .response.stream.message_response import streamed_response
#from .response.stream.completion_response import streamed_response
#from .response.basic.completion_response import response as basic_response
#from random import randint
#import re

logger = logging.getLogger(__name__)

@app.post("/v1/messages")
async def message_completion(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    print(post_json_data)

    model = post_json_data["model"]
    messages = post_json_data["messages"]
    streaming = post_json_data.get("stream", False)
    if len(messages)==1:
        messages = messages[0]["content"]


    settings = {}
    if "options" in post_json_data:
        options = post_json_data["options"]
        settings["temperature"] = options.get("temperature")
        settings["max_tokens"] = options.get("max_tokens")

    if isinstance(messages, str):
        request_msg = messages
    else:
        request_msg = json.dumps(messages, indent=True, ensure_ascii=False)

    response_text = await prompt_completion(request_msg, None, model, **settings)
    print(response_text)
    if not streaming:
        response_object = {
      "content": [
        {
          "text": response_text,
          "type": "text"
        }
      ],
      "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
      "model": model,
      "role": "assistant",
      "stop_reason": "end_turn",
      "stop_sequence": None,
      "type": "message",
      "usage": {
        "input_tokens": 2095,
        "output_tokens": 503
      }
    }
        return JSONResponse(content=response_object)
    else:
        return StreamingResponse(
            streamed_response(response_text, model), media_type="text/event-stream"
        )
