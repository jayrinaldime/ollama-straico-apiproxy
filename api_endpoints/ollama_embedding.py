import json
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from app import app

from backend.embedding import get_embedding_model

from os import environ
from datetime import datetime

logger = logging.getLogger(__name__)

default_embedding_model = environ.get(
    "DEFAULT_EMBEDDING_MODEL", "nomic-ai/nomic-embed-text-v1.5"
)


@app.post("/api/embeddings")
async def ollama_embedding(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    logger.debug(post_json_data)
    embedding_model = post_json_data.get("model", default_embedding_model)

    input_text = post_json_data["prompt"]

    model = get_embedding_model(embedding_model)
    embeddings = model.encode([input_text])
    embed = embeddings[0].tolist()

    return JSONResponse(content={"embedding": embed})


@app.post("/api/embed")
async def ollama_embed(request: Request):
    start_dt = datetime.now()
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    logger.debug(post_json_data)
    embedding_model = post_json_data.get("model", default_embedding_model)

    input_text = post_json_data["input"]
    if type(input_text) == str:
        input_text = [
            input_text,
        ]

    model = get_embedding_model(embedding_model)
    loading_end = datetime.now()
    embeddings = model.encode(input_text)

    embedding_data = []
    for index in range(embeddings.shape[0]):
        embed = embeddings[index].tolist()
        embedding_data.append(embed)
    processing_end = datetime.now()
    total_duration = processing_end - start_dt
    load_duration = loading_end - start_dt
    return JSONResponse(
        content={
            "model": embedding_model,
            "embedding": embedding_data,
            "total_duration": total_duration.total_seconds(),
            "load_duration": load_duration.total_seconds(),
            "prompt_eval_count": 18,
        }
    )
