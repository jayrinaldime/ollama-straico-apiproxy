def response(response, model):
    return {
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
