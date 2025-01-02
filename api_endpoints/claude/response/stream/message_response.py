import asyncio
import uuid
import logging
import json
import time

logger = logging.getLogger(__name__)


def stream_data_response(event_type, msg):
    line1 = f"event: {event_type}\n"
    line2 = "data: " + json.dumps(msg, ensure_ascii=False) + "\n\n"

    return line1 + line2


async def streamed_response(response, model):
    request_id = "msg_" + str(uuid.uuid4())
    logger.debug(f"Response {response}")
    yield stream_data_response(
        "message_start",
        {
            "type": "message_start",
            "message": {
                "id": request_id,
                "type": "message",
                "role": "assistant",
                "model": model,
                "stop_sequence": None,
                "usage": {"input_tokens": 472, "output_tokens": 2},
                "content": [],
                "stop_reason": None,
            },
        },
    )
    time.sleep(0.2)
    yield stream_data_response(
        "content_block_start",
        {
            "type": "message_start",
            "message": {
                "type": "content_block_start",
                "index": 0,
                "content_block": {"type": "text", "text": ""},
            },
        },
    )

    yield stream_data_response("ping", {"type": "ping"})
    for word in response.split(" "):
        yield stream_data_response(
            "content_block_delta",
            {
                "type": "content_block_delta",
                "index": 0,
                "delta": {"type": "text_delta", "text": word + " "},
            },
        )
        # time.sleep(0.05)

    yield stream_data_response(
        "content_block_stop", {"type": "content_block_stop", "index": 0}
    )

    # time.sleep(0.2)
    # yield stream_data_response(
    #     "message_delta",
    #     {"type": "message_delta",
    #       "delta": {"stop_reason": "end_turn", "stop_sequence": None, "output_tokens": 15},
    #       "output_tokens": 15,
    #       "usage": {"output_tokens": 15}}
    # )

    time.sleep(0.2)
    yield stream_data_response(
        "message_stop",
        {
            "type": "message_stop",
        },
    )
