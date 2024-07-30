import time
import json
from app import app, logging
from flask import request, jsonify, Response
from backend import list_model, prompt_completion, user_detail

logger = logging.getLogger(__name__)
MODEL_SIZE = 7365960935


@app.route("/api/version", methods=["GET"])
def ollama_version():
    version = {'version': '0.3.0'}
    logger.info(version)
    return version, 200


@app.route("/api/delete", methods=["DELETE"])
def ollama_delete():
    logger.debug(request.data)
    return "", 200


@app.route("/api/pull", methods=["POST"])
def ollama_pull(x=0):
    logger.debug(f"Pull request {request.data}")
    try:
        is_stream_request = request.json().get("stream") or True
    except:
        is_stream_request = True

    if is_stream_request:
        return Response(generate_ollama_pull_stream(), content_type='application/x-ndjson')
    else:
        return {"status": "success"}, 200


def stream_json_response(response):
    return json.dumps(response) + '\n'


def generate_ollama_pull_stream():
    step_sleep = 0.2
    download_sleep = 0.005
    yield stream_json_response({"status": "pulling manifest"})
    time.sleep(step_sleep)
    for i in range(20):
        yield stream_json_response(
            {
                "status": "pulling ff82381e2bea",
                "digest": "sha256:ff82381e2bea77d91c1b824c7afb83f6fb73e9f7de9dda631bcdbca564aa5435",
                "total": MODEL_SIZE
            }
        )
        time.sleep(download_sleep)
    for i in range(1, 100, 5):
        yield stream_json_response(
            {
                "status": "pulling ff82381e2bea",
                "digest": "sha256:ff82381e2bea77d91c1b824c7afb83f6fb73e9f7de9dda631bcdbca564aa5435",
                "total": MODEL_SIZE,
                "completed": int(MODEL_SIZE * (i / 100))
            }
        )
        time.sleep(download_sleep)

    yield stream_json_response({"status": "verifying sha256 digest"})
    time.sleep(step_sleep)

    yield stream_json_response({"status": "writing manifest"})
    time.sleep(step_sleep)

    yield stream_json_response({"status": "removing any unused layers"})
    time.sleep(step_sleep)

    yield stream_json_response({"status": "success"})


@app.route("/api/show", methods=["POST"])
def show_model_details():
    return jsonify({
        "modelfile": "# Modelfile generated by \"ollama show\"\n# To build a new Modelfile based on this one, replace the FROM line with:\n# FROM llava:latest\n\nFROM /Users/matt/.ollama/models/blobs/sha256:200765e1283640ffbd013184bf496e261032fa75b99498a9613be4e94d63ad52\nTEMPLATE \"\"\"{{ .System }}\nUSER: {{ .Prompt }}\nASSISTANT: \"\"\"\nPARAMETER num_ctx 4096\nPARAMETER stop \"\u003c/s\u003e\"\nPARAMETER stop \"USER:\"\nPARAMETER stop \"ASSISTANT:\"",
        "parameters": "num_keep                       24\nstop                           \"<|start_header_id|>\"\nstop                           \"<|end_header_id|>\"\nstop                           \"<|eot_id|>\"",
        "template": "{{ if .System }}<|start_header_id|>system<|end_header_id|>\n\n{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>\n\n{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>\n\n{{ .Response }}<|eot_id|>",
        "details": {
            "parent_model": "",
            "format": "gguf",
            "family": "llama",
            "families": [
                "llama"
            ],
            "parameter_size": "8.0B",
            "quantization_level": "Q4_0"
        },
        "model_info": {
            "general.architecture": "llama",
            "general.file_type": 2,
            "general.parameter_count": 8030261248,
            "general.quantization_version": 2,
            "llama.attention.head_count": 32,
            "llama.attention.head_count_kv": 8,
            "llama.attention.layer_norm_rms_epsilon": 0.00001,
            "llama.block_count": 32,
            "llama.context_length": 8192,
            "llama.embedding_length": 4096,
            "llama.feed_forward_length": 14336,
            "llama.rope.dimension_count": 128,
            "llama.rope.freq_base": 500000,
            "llama.vocab_size": 128256,
            "tokenizer.ggml.bos_token_id": 128000,
            "tokenizer.ggml.eos_token_id": 128009,
            "tokenizer.ggml.merges": [],  # populates if `verbose=true`
            "tokenizer.ggml.model": "gpt2",
            "tokenizer.ggml.pre": "llama-bpe",
            "tokenizer.ggml.token_type": [],  # populates if `verbose=true`
            "tokenizer.ggml.tokens": []  # populates if `verbose=true`
        }
    })


@app.route("/api/tags", methods=["GET"])
def list_straico_models():
    models = list_model().get("data")
    if models is None:
        return jsonify({"models": []})

    if "chat" in models:
        models = models["chat"]

    return jsonify({
        "models": [
            {
                "name": m["name"],
                # Open Web UI does not work without explicit tag
                "model": m["model"] if ":" in m["model"] else m["model"] + ":latest",
                "modified_at": "2023-11-04T14:56:49.277302595-07:00",
                "size": MODEL_SIZE,
                "digest": m["model"],  # "9f438cb9cd581fc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
                "details": {
                    "format": "gguf",
                    "family": "llama",
                    "families": None,
                    "parameter_size": "",
                    "quantization_level": "Q4_0"
                }
            } for m in models]
    })


@app.route("/api/generate", methods=["POST"])
def ollamagenerate():
    try:
        msg = request.json
    except:
        msg = json.loads(request.data.decode())

    logger.debug(msg)
    request_msg = msg["prompt"]
    model = msg.get("model")
    if msg.get("stream") == False:
        response = prompt_completion(msg["prompt"], model)
        return {
            "model": model,
            "created_at": "2023-08-04T19:22:45.499127Z",
            "response": response,
            "done": True,
            "total_duration": 10706818083,
            "load_duration": 6338219291,
            "prompt_eval_count": 26,
            "prompt_eval_duration": 130079000,
            "eval_count": 259,
            "eval_duration": 4232710000
        }

    return Response(generate_ollama_stream(request_msg, model), content_type='application/x-ndjson')


@app.route("/api/chat", methods=["POST"])
def ollamachat():
    try:
        msg = request.json
    except:
        msg = json.loads(request.data.decode())

    model = msg["model"]
    tools = msg.get("tools")
    messages = msg["messages"]
    if tools and len(tools) != 0:
        parent_tool = [
            {
                "role": "system",
                "tools": tools,
                "content": """
If you need to use a tool to answer please use the defined tools. 
Assuming the function is 
```
{"tools":[{"type":"function","function":{"name":"get_current_weather","description":"Get the current weather for a location","parameters":{"type":"object","properties":{"location":{"type":"string","description":"The location to get the weather for, e.g. San Francisco, CA"},"format":{"type":"string","description":"The format to return the weather in, e.g. 'celsius' or 'fahrenheit'","enum":["celsius","fahrenheit"]}},"required":["location","format"]}}}]}
```
When you do use a function your output should like
``` 
{"tool_calls":[{"function":{"name":"get_current_weather","arguments":{"format":"celsius","location":"Paris, FR"}}}]}
``` 
You must answer by exactly following the provided instructions. Do not add any additional comments or explanations.
Do not add "Here is..." or anything like that.

Act like a script, you are given an optional input and the instructions to perform, you answer with the output of the requested task.

Please only output plain json  
                    """
            }
        ]
        messages = parent_tool + messages

    if "stream" in msg:
        streaming = msg.get("stream")
    else:
        streaming = True

    logger.debug(msg)
    logger.debug(model)
    if type(messages) == list and len(messages) ==1 and type(messages[0]) == dict and "content" in messages[0]:
        messages = messages[0]["content"]
    request_msg = json.dumps(messages, indent=True)
    response = prompt_completion(request_msg, model)
    try:
        response = json.loads(response)
        response_type = type(response)
        if response_type == dict and "content" in response:
            response = response["content"]
        elif response_type == list and len(response) > 0 and type(response[0]) == dict and "content" in response[0]:
            response = response[0]["content"]
    except:
        pass
    response_type = type(response)

    original_response = response
    if tools is not None and len(tools) != 0:

        if response_type == str:
            response = response.strip()
            if response.startswith("```json") and response.endswith("```"):
                response = response[7:-3].strip()
                response = json.loads(response)
            elif response.startswith("```") and response.endswith("```"):
                response = response[3:-3].strip()
                response = json.loads(response)
            else:
                try:
                    response = json.loads(response)
                except:
                    pass
        if type(response) == list and len(response) > 0:
            response = response[0]

        if type(response) == dict and "tool_calls" in response:
            return {
                "model": model,
                "created_at": "2024-07-22T20:33:28.123648Z",
                "message": {
                    "role": "assistant",
                    "content": "",
                    "tool_calls": response["tool_calls"]
                },
                "done_reason": "stop",
                "done": True,
                "total_duration": 885095291,
                "load_duration": 3753500,
                "prompt_eval_count": 122,
                "prompt_eval_duration": 328493000,
                "eval_count": 33,
                "eval_duration": 552222000
            }, 200

    if len(messages) > 1 and response_type == str:
        response = response.strip()
        if response.startswith("```json") and response.endswith("```"):
            response = response[7:-3].strip()
            original_response = json.loads(response)
        elif response.startswith("```") and response.endswith("```"):
            response = response[3:-3].strip()
            original_response = json.loads(response)
        else:
            try:
                original_response = json.loads(response)

            except:
                pass

            if type(original_response) == dict and "role" in original_response and original_response[
                "role"] == "assistant" and "content" in original_response:
                original_response = original_response["content"]

    if streaming:
        return Response(response_stream(model, original_response, is_tool=False),
                        content_type='application/x-ndjson')
    else:
        return {
            "model": model,
            "created_at": "2023-12-12T14:13:43.416799Z",
            "message": {
                "role": "assistant",
                "content": original_response
            },
            "done": True,
            "total_duration": 5191566416,
            "load_duration": 2154458,
            "prompt_eval_count": 26,
            "prompt_eval_duration": 383809000,
            "eval_count": 298,
            "eval_duration": 4799921000
        }, 200


@app.route("/api/user", methods=["GET"])
def user():
    models = user_detail().get("data", {})
    return jsonify({"user": models})


def json_stream_json_dump(obj):
    return json.dumps(obj) + "\n"


def response_stream(model, response, is_tool=False):
    if is_tool:
        pass
    if is_tool:
        yield json_stream_json_dump({
            "model": model,
            "created_at": "2023-12-12T14:13:43.416799Z",
            "message": {
                "role": "assistant",
                "content": "",
                "tool_calls": response
            },
            "done": False,
            "total_duration": 5191566416,
            "load_duration": 2154458,
            "prompt_eval_count": 26,
            "prompt_eval_duration": 383809000,
            "eval_count": 298,
            "eval_duration": 4799921000
        })
    else:
        yield json_stream_json_dump({
            "model": model,
            "created_at": "2023-12-12T14:13:43.416799Z",
            "message": {
                "role": "assistant",
                "content": response
            },
            "done": False,
            "total_duration": 5191566416,
            "load_duration": 2154458,
            "prompt_eval_count": 26,
            "prompt_eval_duration": 383809000,
            "eval_count": 298,
            "eval_duration": 4799921000
        })

    yield json_stream_json_dump({
        "model": model,
        "created_at": "2023-12-12T14:13:43.416799Z",
        "message": {
            "role": "assistant",
            "content": ""
        },
        "done_reason": "stop",
        "done": True,
        "total_duration": 5191566416,
        "load_duration": 2154458,
        "prompt_eval_count": 26,
        "prompt_eval_duration": 383809000,
        "eval_count": 298,
        "eval_duration": 4799921000
    })


def generate_ollama_stream(msg, model):
    logger.debug(msg)
    response = prompt_completion(msg, model)

    #for i in range(0, len(response), 5):
    r = json_stream_json_dump({
            "model": model,
            "created_at": "2023-12-12T14:14:43.416799Z",
            "response": response,#[i:i + 5],
            "done": False
        })
    yield r
        #time.sleep(0.1)

    yield json_stream_json_dump({
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
        "eval_duration": 4232710000
    })