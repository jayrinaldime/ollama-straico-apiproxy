import asyncio
import json
from app import app, logging
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from backend import list_model, list_agents, user_detail, delete_agent, list_agents
from .response.stream import completion_response

logger = logging.getLogger(__name__)
MODEL_SIZE = 7365960935


@app.get("/api/version")
def ollama_version():
    version = {"version": "0.5.1"}
    logger.info(version)
    return JSONResponse(content=version)


@app.delete("/api/delete")
async def ollama_delete(request: Request):
    data = await request.json()
    logger.debug(data)
    model_name = data["name"]
    if model_name.startswith("agent/"):
        model_id = model_name.split(":")[-1]
        r = await delete_agent(model_id)

    return ""


@app.post("/api/pull")
async def ollama_pull(request: Request):
    logger.debug(f"Pull request {await request.body()}")
    try:
        is_stream_request = (await request.json()).get("stream") or True
    except:
        is_stream_request = True

    if is_stream_request:
        return StreamingResponse(
            generate_ollama_pull_stream(), media_type="application/x-ndjson"
        )
    else:
        return JSONResponse(content={"status": "success"})


# def stream_json_response(response):
#     return json.dumps(response) + "\n"


async def generate_ollama_pull_stream():
    step_sleep = 0.2
    download_sleep = 0.005
    yield completion_response.json_stream_json_dump({"status": "pulling manifest"})
    await asyncio.sleep(step_sleep)
    for i in range(20):
        yield completion_response.json_stream_json_dump(
            {
                "status": "pulling ff82381e2bea",
                "digest": "sha256:ff82381e2bea77d91c1b824c7afb83f6fb73e9f7de9dda631bcdbca564aa5435",
                "total": MODEL_SIZE,
            }
        )
        await asyncio.sleep(download_sleep)
    for i in range(1, 100, 5):
        yield completion_response.json_stream_json_dump(
            {
                "status": "pulling ff82381e2bea",
                "digest": "sha256:ff82381e2bea77d91c1b824c7afb83f6fb73e9f7de9dda631bcdbca564aa5435",
                "total": MODEL_SIZE,
                "completed": int(MODEL_SIZE * (i / 100)),
            }
        )
        await asyncio.sleep(download_sleep)

    yield completion_response.json_stream_json_dump(
        {"status": "verifying sha256 digest"}
    )
    await asyncio.sleep(step_sleep)

    yield completion_response.json_stream_json_dump({"status": "writing manifest"})
    await asyncio.sleep(step_sleep)

    yield completion_response.json_stream_json_dump(
        {"status": "removing any unused layers"}
    )
    await asyncio.sleep(step_sleep)

    yield completion_response.json_stream_json_dump({"status": "success"})


@app.post("/api/show")
def show_model_details():
    return JSONResponse(
        content={
            "modelfile": '# Modelfile generated by "ollama show"\n# To build a new Modelfile based on this one, replace the FROM line with:\n# FROM llava:latest\n\nFROM /Users/matt/.ollama/models/blobs/sha256:200765e1283640ffbd013184bf496e261032fa75b99498a9613be4e94d63ad52\nTEMPLATE """{{ .System }}\nUSER: {{ .Prompt }}\nASSISTANT: """\nPARAMETER num_ctx 4096\nPARAMETER stop "\u003c/s\u003e"\nPARAMETER stop "USER:"\nPARAMETER stop "ASSISTANT:"',
            "parameters": 'num_keep                       24\nstop                           "<|start_header_id|>"\nstop                           "<|end_header_id|>"\nstop                           "<|eot_id|>"',
            "template": "{{ if .System }}<|start_header_id|>system<|end_header_id|>\n\n{{ .System }}<|eot_id|>{{ end }}{{ if .Prompt }}<|start_header_id|>user<|end_header_id|>\n\n{{ .Prompt }}<|eot_id|>{{ end }}<|start_header_id|>assistant<|end_header_id|>\n\n{{ .Response }}<|eot_id|>",
            "details": {
                "parent_model": "",
                "format": "gguf",
                "family": "llama",
                "families": ["llama"],
                "parameter_size": "8.0B",
                "quantization_level": "Q4_0",
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
                "tokenizer.ggml.tokens": [],  # populates if `verbose=true`
            },
        }
    )


@app.get("/api/tags")
async def list_straico_models():
    models = await list_model()
    if models is None:
        return JSONResponse(content={"models": []})

    if "chat" in models:
        models = models["chat"]

    response_models = [
        {
            "name": m["name"],
            # Open Web UI does not work without explicit tag
            "model": (m["model"] if ":" in m["model"] else m["model"] + ":latest"),
            "modified_at": "2023-11-04T14:56:49.277302595-07:00",
            "size": MODEL_SIZE,
            "digest": m[
                "model"
            ],  # "9f438cb9cd581fc025612d27f7c1a6669ff83a8bb0ed86c94fcf4c5440555697",
            "details": {
                "format": "gguf",
                "family": "llama",
                "families": None,
                "parameter_size": "",
                "quantization_level": "Q4_0",
            },
        }
        for m in models
    ]
    agents = await list_agents()
    if agents is not None or len(agents) > 0:
        response_models += [
            {
                "name": f"Agent: {m["name"].strip()} ({m['_id']})",
                # Open Web UI does not work without explicit tag
                "model": (f"agent/{m['name'].strip()}:{m['_id']}"),
                "modified_at": m["updatedAt"].split(".")[0] + ".277302595-07:00",
                "size": MODEL_SIZE,
                "digest": m["_id"],
                "details": {
                    "format": "gguf",
                    "family": "llama",
                    "families": None,
                    "parameter_size": "",
                    "quantization_level": "Q4_0",
                },
            }
            for m in agents
        ]

    return JSONResponse(content={"models": response_models})


@app.get("/api/user")
async def user():
    models = await user_detail()
    return JSONResponse(content=models)


@app.get("/api/model_list")
async def straico_models():
    models = await list_model()
    return JSONResponse(content=models)
