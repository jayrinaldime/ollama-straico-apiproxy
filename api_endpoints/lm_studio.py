import json
from app import app, logging
from flask import request, jsonify, Response
from backend import list_model, prompt_completion
import uuid

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
                "delta": {
                    "role": "assistant",
                    "content": ""
                },
                "finish_reason": None
            }
        ]
    }

def end_response(rid, model):
    return {
        "id": f"chatcmpl-{rid}",
        "object": "chat.completion.chunk",
        "created": 1716456766,
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }
        ]
    }

def stream_data_response(msg):
    return "data: " + json.dumps(msg) + '\n'
def generate_json_data(msg, model):
    request_id = str(uuid.uuid4())
    yield stream_data_response(start_response(request_id, model))
    d = prompt_completion(json.dumps(msg, indent=True), model)
    logger.debug(f"Response {d}")

    yield stream_data_response({
        "id": f"chatcmpl-{request_id}",
        "object": "chat.completion.chunk",
        "created": 1716456766,
        "model": model,
        "choices": [
            {
                "index": 0,
                "delta": {
                    "role": "assistant",
                    "content": d
                },
                "finish_reason": None
            }
        ]
    })

    yield stream_data_response(end_response(request_id, model))

    yield "[DONE]"

@app.route('/chat/completions', methods=['POST'])
@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    logger.debug(request.json)
    post_json_data = request.json
    msg = post_json_data["messages"]
    model = post_json_data.get("model") or "openai/gpt-3.5-turbo-0125"
    if request.method == 'POST':
        return Response(generate_json_data(msg,model), content_type='text/event-stream')
    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route('/v1/completions', methods=['POST'])
def completions():
    msg = request.json["prompt"]
    logger.debug(msg)
    if request.method == 'POST':
        return Response(generate_json_data(msg), content_type='text/event-stream')
    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route('/v1/models', methods=["GET"])
def lmstudio_list_model():
    """
    {'name': 'Anthropic: Claude 3 Haiku',
   'model': 'anthropic/claude-3-haiku:beta',
   'pricing': {'coins': 1, 'words': 100}}
    """
    models = [{
                "id": model["model"],
                "object": "model",
                "owned_by": model["name"].split(":")[0],
                "permission": [
                    {}
                ]
            } for model in list_model()["data"]]
    response = {
        "data": models,
        "object": "list"
    }
    return jsonify(response)

