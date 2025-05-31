import uuid
import logging
import json

logger = logging.getLogger(__name__)


def stream_data_response(msg):
    return "data: " + json.dumps(msg, ensure_ascii=False) + "\n\n"


def end_response(rid, model, finish_reason="stop"):
    return {
        "id": f"chatcmpl-{rid}",
        "object": "chat.completion.chunk",
        "created": 1716456766,
        "model": model,
        "system_fingerprint": model,
        "choices": [{"index": 0, "delta": {}, "finish_reason": finish_reason}],
    }


def streamed_response_toolcall(tool_call, model):
    request_id = str(uuid.uuid4())
    tool_call["tool_calls"][0]["index"] = 0

    yield stream_data_response(
        {
            "id": f"chatcmpl-{request_id}",
            "object": "chat.completion.chunk",
            "created": 1748531779,
            "model": model,
            "system_fingerprint": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {"role": "assistant", "content": "\n\n"},
                    "finish_reason": None,
                }
            ],
        }
    )
    yield stream_data_response(
        {
            "id": f"chatcmpl-{request_id}",
            "object": "chat.completion.chunk",
            "created": 1748531779,
            "model": model,
            "system_fingerprint": model,
            "choices": [
                {
                    "index": 0,
                    "delta": {"tool_calls": tool_call["tool_calls"]},
                    "finish_reason": None,
                    "logprobs": None,
                }
            ],
        }
    )

    yield stream_data_response(
        end_response(request_id, model, finish_reason="tool_calls")
    )

    yield "data: [DONE]\n\n"


def streamed_response(response, model):
    request_id = str(uuid.uuid4())
    logger.debug(f"Response {response}")

    yield stream_data_response(
        {
            "id": f"chatcmpl-{request_id}",
            "object": "chat.completion.chunk",
            "created": 1716456766,
            "model": model,
            "system_fingerprint": model,
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
