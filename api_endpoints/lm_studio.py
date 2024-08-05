import json
import time
import uuid
import logging

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse, StreamingResponse
from app import app
from aio_straico import aio_straico_client


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


@app.post("/chat/completions")
@app.post("/v1/chat/completions")
async def chat_completions(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())

    msg = post_json_data["messages"]
    model = post_json_data.get("model") or "openai/gpt-3.5-turbo-0125"
    streaming = post_json_data.get("stream", True)
    async with aio_straico_client() as client:
        response = await client.prompt_completion(model, json.dumps(msg, indent=True))
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
async def completions(request: Request):
    post_json_data = await request.json()
    msg = post_json_data["prompt"]
    model = post_json_data.get("model") or "openai/gpt-3.5-turbo-0125"
    logger.debug(msg)

    async with aio_straico_client() as client:
        response = await client.prompt_completion(model, msg)
        if request.method == "POST":
            return StreamingResponse(
                generate_json_data(msg, model), content_type="text/event-stream"
            )

        return JSONResponse(content={"error": "Method not allowed"}, status_code=405)


@app.get("/api/models")
@app.get("/v1/api/models")
@app.get("/v1/models")
@app.get("/models")
async def lmstudio_list_models():
    """
     {'name': 'Anthropic: Claude 3 Haiku',
    'model': 'anthropic/claude-3-haiku:beta',
    'pricing': {'coins': 1, 'words': 100}}
    """

    async with aio_straico_client() as client:
        models = await client.models(v=1)
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
