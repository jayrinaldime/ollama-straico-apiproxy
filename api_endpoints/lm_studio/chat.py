import json
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from app import app, logging
from backend.straico import prompt_completion
from .response.stream.completion_response import streamed_response
from .response.basic.completion_response import response as basic_response

logger = logging.getLogger(__name__)

def _get_msg_text(content):
    text = []
    for content_object in content:
        if content_object["type"] == "text":
            text.append(content_object["text"])
    return "\n".join(text)


def _get_msg_image(content):
    images = []
    for content_object in content:
        if content_object["type"] == "image_url":
            data = content_object["image_url"]["url"]
            starting_index = data.find(",")
            images.append(data[starting_index:])
    return images

@app.post("/chat/completions")
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())

    streaming = post_json_data.get("stream", False)
    model = post_json_data.get("model") or "openai/gpt-3.5-turbo-0125"
    msg = post_json_data["messages"]
    logger.debug(msg)
    logger.debug(model)
    if (
        type(msg) == list
        and len(msg) == 1
        and type(msg[0]) == dict
        and "content" in msg[0]
    ):
        if type(msg[0]["content"]) == str:
            response = await prompt_completion(msg[0]["content"], model=model)
        else:
            images = _get_msg_image(msg[0]["content"])
            msg = _get_msg_text(msg[0]["content"])
            response = await prompt_completion(msg, images=images, model=model)
    else:
        response = await prompt_completion(json.dumps(msg, indent=True), model=model)

    if streaming:
        # generate_json_data
        return StreamingResponse(
            streamed_response(response, model), media_type="text/event-stream"
        )

    return JSONResponse(
        content=basic_response(response, model)
    )

@app.post("/v1/completions")
async def completions(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    msg = post_json_data["prompt"]
    model = post_json_data.get("model") or "openai/gpt-3.5-turbo-0125"
    logger.debug(msg)
    response = await prompt_completion(msg, model=model)

    return StreamingResponse(
        streamed_response(response, model), content_type="text/event-stream"
    )
