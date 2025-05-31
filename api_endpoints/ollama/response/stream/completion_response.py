from backend import prompt_completion
from app import logging
import json

logger = logging.getLogger(__name__)


def json_stream_json_dump(obj):
    return json.dumps(obj, ensure_ascii=False) + "\n"


async def response_stream(model, response, thinking_text, is_tool=False):
    if is_tool:
        pass
    if is_tool:
        yield json_stream_json_dump(
            {
                "model": model,
                "created_at": "2023-12-12T14:13:43.416799Z",
                "message": {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": response,
                    "thinking": thinking_text,
                },
                "done": False,
                "total_duration": 5191566416,
                "load_duration": 2154458,
                "prompt_eval_count": 26,
                "prompt_eval_duration": 383809000,
                "eval_count": 298,
                "eval_duration": 4799921000,
            }
        )
    else:
        yield json_stream_json_dump(
            {
                "model": model,
                "created_at": "2023-12-12T14:13:43.416799Z",
                "message": {
                    "role": "assistant",
                    "content": response,
                    "thinking": thinking_text,
                },
                "done": False,
                "total_duration": 5191566416,
                "load_duration": 2154458,
                "prompt_eval_count": 26,
                "prompt_eval_duration": 383809000,
                "eval_count": 298,
                "eval_duration": 4799921000,
            }
        )

    yield json_stream_json_dump(
        {
            "model": model,
            "created_at": "2023-12-12T14:13:43.416799Z",
            "message": {"role": "assistant", "content": ""},
            "done_reason": "stop",
            "done": True,
            "total_duration": 5191566416,
            "load_duration": 2154458,
            "prompt_eval_count": 26,
            "prompt_eval_duration": 383809000,
            "eval_count": 298,
            "eval_duration": 4799921000,
        }
    )


async def generate_ollama_stream(msg, model):
    r = json_stream_json_dump(
        {
            "model": model,
            "created_at": "2023-12-12T14:14:43.416799Z",
            "response": msg,  # [i:i + 5],
            "done": False,
        }
    )
    yield r

    yield json_stream_json_dump(
        {
            "model": model,
            "created_at": "2023-12-12T14:14:43.416799Z",
            "response": "",
            "done": True,
            "done_reason": "stop",
            "total_duration": 10706818083,
            "load_duration": 6338219291,
            "prompt_eval_count": 26,
            "prompt_eval_duration": 130079000,
            "eval_count": 259,
            "eval_duration": 4232710000,
        }
    )
