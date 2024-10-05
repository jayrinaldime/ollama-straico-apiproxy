import uuid
import logging
import json

logger = logging.getLogger(__name__)

def stream_data_response(msg):
    return "data: " + json.dumps(msg) + "\n\n"

def end_response(rid, model):
    return {
        "id": f"chatcmpl-{rid}",
        "object": "chat.completion.chunk",
        "created": 1716456766,
        "model": model,
        "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
    }


def streamed_response(response, model):
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
