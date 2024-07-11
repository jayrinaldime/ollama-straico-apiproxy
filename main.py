
from flask import Flask, request, jsonify, Response
import requests
import pprint
import uuid
import json
import os
app = Flask(__name__)

def start_response(rid):
    START_RESPONSE = {
        "id": f"chatcmpl-{rid}",
        "object": "chat.completion.chunk",
        "created": 1716456766,
        "model": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q8_0.gguf",
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
    return START_RESPONSE

def end_response(rid):
    END_RESPONSE = {
        "id": f"chatcmpl-{rid}",
        "object": "chat.completion.chunk",
        "created": 1716456766,
        "model": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q8_0.gguf",
        "choices": [
            {
                "index": 0,
                "delta": {},
                "finish_reason": "stop"
            }
        ]
    }
    return END_RESPONSE


def generate_json_data(msg, model):
    request_id = str(uuid.uuid4())
    yield "data: " + json.dumps(start_response(request_id)) + '\n'
    d = straico_llm(json.dumps(msg, indent=True), model)
    print("Response", d)

    yield "data: " + json.dumps({
    "id": f"chatcmpl-{request_id}",
    "object": "chat.completion.chunk",
    "created": 1716456766,
    "model": "lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF/Meta-Llama-3-8B-Instruct-Q8_0.gguf",
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
})+ '\n'
    yield "data: "+ json.dumps(end_response(request_id)) + '\n'

    yield "[DONE]"


STRAICO_API_KEY = os.environ.get("STRAICO_API_KEY") or ""

def generate_ollama_stream(msg, model):
    print(msg)
    r =  json.dumps({
  "model": model,
  "created_at": "2023-12-12T14:13:43.416799Z",
  "response": "\n",
  "done": False
    }, indent=False).replace('\n', '')+ "\n"
    #print(r)
    yield r
    response = straico_llm(msg, model)

    r = {
        "model": model,
        "created_at": "2023-12-12T14:14:43.416799Z",
        "response": response,
        "done": False}
    r = json.dumps(r, indent=False).replace('\n', '')+ "\n"
    print(r)
    yield r
    r = json.dumps({
        "model": model,
        "created_at": "2023-12-12T14:14:43.416799Z",
        "response": "",
        "done": True,
        "context": [1, 2, 3],
        "total_duration": 10706818083,
        "load_duration": 6338219291,
        "prompt_eval_count": 26,
        "prompt_eval_duration": 130079000,
        "eval_count": 259,
        "eval_duration": 4232710000
    }, indent=False).replace('\n', '')+ "\n"

    #print(r)
    yield r


def straico_llm(msg: str, model="openai/gpt-3.5-turbo-0125"):
    r = requests.post("https://api.straico.com/v0/prompt/completion",
              headers = {"Authorization": f"Bearer {STRAICO_API_KEY}"},
              data = {"model": model,
                      "message": msg})
    return r.json()["data"]["completion"]["choices"][-1]["message"]["content"]

@app.route('/chat/completions', methods=['POST'])
@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    pprint.pprint(request.json)
    msg = request.json["messages"]
    model = request.json.get("model") or "openai/gpt-3.5-turbo-0125"
    if request.method == 'POST':
        return Response(generate_json_data(msg,model), content_type='text/event-stream')
    else:
        return jsonify({"error": "Method not allowed"}), 405

@app.route('/v1/completions', methods=['POST'])
def completions():
    # import pprint
    # pprint.print(request.json)
    msg = request.json["prompt"]
    print(msg)
    pprint.pprint(msg)
    if request.method == 'POST':
        return Response(generate_json_data(msg), content_type='text/event-stream')
    else:
        return jsonify({"error": "Method not allowed"}), 405

def request_straico_models():
    r = requests.get("https://api.straico.com/v0/models",
                     headers={"Authorization": f"Bearer {STRAICO_API_KEY}"}, )
    return r.json()


def response_stream(model, response):
    yield json.dumps({
  "model": model,
  "created_at": "2023-12-12T14:13:43.416799Z",
  "message": {
    "role": "assistant",
    "content":response
  },
  "done": False,
  "total_duration": 5191566416,
  "load_duration": 2154458,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 383809000,
  "eval_count": 298,
  "eval_duration": 4799921000
}, indent=False).replace('\n', '')+ "\n"

    yield json.dumps({
        "model": model,
        "created_at": "2023-12-12T14:13:43.416799Z",
        "done": True,
        "total_duration": 5191566416,
        "load_duration": 2154458,
        "prompt_eval_count": 26,
        "prompt_eval_duration": 383809000,
        "eval_count": 298,
        "eval_duration": 4799921000
    }, indent=False).replace('\n', '') + "\n"


@app.route("/api/chat", methods=["POST"])
def ollamachat():
    try:
        msg = request.json
        model = msg["model"]
    except:
        msg = json.loads(request.data.decode())

    if "stream" in msg:
        streaming = msg.get("stream")
    else:
        streaming = True

    if ":" in msg["model"]:
        model = msg["model"].split(":")[0]
    pprint.pprint(msg)
    print(model)
    request_msg = json.dumps(msg["messages"], indent=True)
    response = straico_llm(request_msg, model)
    try:
        response = json.loads(response)
        response = response[0]["content"]
    except:
        pass
#     return json.dumps({
#     "id": "chatcmpl-641",
#     "object": "chat.completion",
#     "created": 1709741623,
#     "model": model,
#     "system_fingerprint": "fp_ollama",
#     "choices": [
#         {
#             "index": 0,
#             "message": {
#                 "role": "assistant",
#                 "content": response
#             },
#             "finish_reason": "stop"
#         }
#     ],
#     "usage": {
#         "prompt_tokens": 12,
#         "completion_tokens": 11,
#         "total_tokens": 23
#     }
# }, indent=False).replace('\n', '')+ "\n"
    if streaming:
        return Response(response_stream(model,response), content_type='application/json')
    else:
        return {
  "model": model,
  "created_at": "2023-12-12T14:13:43.416799Z",
  "message": {
    "role": "assistant",
    "content":response
  },
  "done": True,
  "total_duration": 5191566416,
  "load_duration": 2154458,
  "prompt_eval_count": 26,
  "prompt_eval_duration": 383809000,
  "eval_count": 298,
  "eval_duration": 4799921000
}, 200


@app.route("/api/generate", methods=["POST"])
def ollamagenerate():
    try:
        msg = request.json
    except:
        msg = json.loads(request.data.decode())

    pprint.pprint(msg)
    request_msg = msg["prompt"]
    model = msg.get("model")
    if msg.get("stream") == False:
        response = straico_llm(msg["prompt"], model)
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
    return Response(generate_ollama_stream(request_msg, model), content_type='application/json')


@app.route("/api/tags", methods=["GET"])
def list_straico_models():
    models = request_straico_models()["data"]
    return jsonify({
  "models": [
    {
      "name": "s-"+m["model"]+":latest",
      "model": m["model"]+":latest",
      "modified_at": "2023-11-04T14:56:49.277302595-07:00",
      "size": 7365960935,
      "digest": m["model"], #"9f438cb9cd581fc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
      "details": {
        "format": "gguf",
        "family": "llama",
        "families": None,
        "parameter_size": "",
        "quantization_level": "Q4_0"
      }
    } for m in models] })

import time
def generate_ollama_pull_stream():

    yield '{"status":"pulling manifest"}\n'
    time.sleep(0.5)
    yield '''{"status": "downloading sha256:fd52b10ee3ee9d753b9ed07a6f764ef2d83628fde5daf39a3d84b86752902182",
     "digest": "sha256:fd52b10ee3ee9d753b9ed07a6f764ef2d83628fde5daf39a3d84b86752902182", "total": 455,
     "completed": 455}\n'''
    time.sleep(0.5)
    yield '''{{"status": "verifying sha256 digest"}\n'''
    time.sleep(0.5)
    yield '''{{"status": "writing manifest"}\n'''
    time.sleep(0.5)
    yield '''{{"status": "removing any unused layers"}\n'''
    time.sleep(0.5)
    yield '''{{"status": "success"}\n'''


@app.route("/api/pull", methods=["POST"])
def ollamapull():
    print(request.data)
    return Response(generate_ollama_pull_stream(), content_type='application/x-ndjson')

@app.route("/api/delete", methods=["DELETE"])
def ollamadelete():
    print(request.data)
    return "",200

@app.route("/api/version", methods=["GET"])
def ollamaversion():
    return {'version': '0.1.41'}, 200



if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=3214)