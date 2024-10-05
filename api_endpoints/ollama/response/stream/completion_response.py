from backend import prompt_completion
from app import logging
import json

logger = logging.getLogger(__name__)

def json_stream_json_dump(obj):
    return json.dumps(obj) + "\n"

async def response_stream(model, response, is_tool=False):
    if is_tool:
        pass
    if is_tool:
        yield json_stream_json_dump(
            {
                "model": model,
                "created_at": "2023-12-12T14:13:43.416799Z",
                "message": {"role": "assistant", "content": "", "tool_calls": response},
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
                "message": {"role": "assistant", "content": response},
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

import logging
async def generate_ollama_stream(msg, model):
    logger.debug(msg)
    response = await prompt_completion(msg, model=model)

    # for i in range(0, len(response), 5):
    r = json_stream_json_dump(
        {
            "model": model,
            "created_at": "2023-12-12T14:14:43.416799Z",
            "response": response,  # [i:i + 5],
            "done": False,
        }
    )
    yield r
    # time.sleep(0.1)

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
