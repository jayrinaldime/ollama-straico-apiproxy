import json
import tempfile
import uuid
import logging

from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from app import app
from backend.straico import prompt_completion, list_model, image_generation
from aio_straico.api.v0 import ImageSize
from base64 import encodebytes

logger = logging.getLogger(__name__)


def start_response(rid, model):
    return {
        "id": f"chatcmpl-{rid}",
        "object": "chat.completion.chunk",
        "created": 1716456766,
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {"role": "assistant", "content": ""},
                "finish_reason": None,
            }
        ],
    }


def end_response(rid, model):
    return {
        "id": f"chatcmpl-{rid}",
        "object": "chat.completion.chunk",
        "created": 1716456766,
        "model": model,
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }


def stream_data_response(msg):
    return "data: " + json.dumps(msg) + "\n\n"


async def generate_json_data(response, model):
    request_id = str(uuid.uuid4())
    logger.debug(f"Response {response}")

    yield stream_data_response(
        {
            "id": f"chatcmpl-{request_id}",
            "object": "chat.completion.chunk",
            "created": 1716456766,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": response},
                    "finish_reason": None,
                }
            ],
        }
    )

    yield stream_data_response(end_response(request_id, model))

    yield "data: [DONE]\n\n"


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
@app.post("/lmstudio/chat/completions")
@app.post("/lmstudio/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())

    streaming = post_json_data.get("stream", False)
    if "tools" in post_json_data:
        streaming = False

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
        return StreamingResponse(
            generate_json_data(response, model), media_type="text/event-stream"
        )

    return JSONResponse(
        content={
            "id": "chatcmpl-gg711phlqdwixyxif16bm",
            "object": "chat.completion",
            "created": 1722418755,
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": response},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 426,
                "completion_tokens": 65,
                "total_tokens": 491,
            },
        }
    )


@app.post("/v1/completions")
@app.post("lmstudio/v1/completions")
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
        generate_json_data(response, model), content_type="text/event-stream"
    )


@app.get("/api/models")
@app.get("/v1/api/models")
@app.get("/v1/models")
@app.get("/models")
@app.get("/lmstudio/api/models")
@app.get("/lmstudio/v1/api/models")
@app.get("/lmstudio/v1/models")
@app.get("/lmstudio/models")
async def lmstudio_list_models():
    """
     {'name': 'Anthropic: Claude 3 Haiku',
    'model': 'anthropic/claude-3-haiku:beta',
    'pricing': {'coins': 1, 'words': 100}}
    """

    models = await list_model()
    if models is None:
        return JSONResponse(content={"models": []})

    if "chat" in models:
        models = models["chat"]

    models = [
        {
            "id": model["model"],
            "object": "model",
            "owned_by": model["name"].split(":")[0],
            "permission": [{}],
        }
        for model in models
    ]
    response = {"data": models, "object": "list"}
    return JSONResponse(content=response)


@app.post("/v1/images/generations")
@app.post("/lmstudio/v1/images/generations")
async def lm_image_generation(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    logger.debug(post_json_data)

    # model = post_json_data.get("model")
    # if model != "openai/dall-e-3":
    model = "openai/dall-e-3"
    prompt = post_json_data.get("prompt")
    n = int(post_json_data.get("n", "1"))
    size = post_json_data.get("size", "512x512")
    x, y = size.strip().lower().split("x")
    if x == y:
        size = ImageSize.square
    elif x > y:
        size = ImageSize.landscape
    elif x < y:
        size = ImageSize.portrait

    with tempfile.TemporaryDirectory() as directory:
        images = await image_generation(
            model=model, n=n, prompt=prompt, size=size, directory=directory
        )
        encoded_images = []

        for image_path in images:
            with image_path.open("rb") as reader:
                bin_image = reader.read(-1)
                data_base64 = encodebytes(bin_image).decode()
                encoded_images.append({"b64_json": data_base64})

    return JSONResponse(content={"created": 1589478378, "data": encoded_images})
