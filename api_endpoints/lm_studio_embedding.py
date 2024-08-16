import json
import logging

from fastapi import Request
from fastapi.responses import JSONResponse
from app import app

from backend.embedding import get_embedding_model

from os import environ

logger = logging.getLogger(__name__)

default_embedding_model = environ.get(
    "DEFAULT_EMBEDDING_MODEL", "nomic-ai/nomic-embed-text-v1.5"
)


@app.post("/v1/embeddings")
async def lm_studio_embedding(request: Request):
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
    embeddings = model.encode(input_text)
    embedding_data = []
    for index in range(embeddings.shape[0]):
        embed = embeddings[index].tolist()
        embedding_data.append(
            {"object": "embedding", "embedding": embed, "index": index}
        )
    return JSONResponse(
        content={
            "object": "list",
            "data": embedding_data,
            "model": embedding_model,
            "usage": {"prompt_tokens": 0, "total_tokens": 0},
        }
    )
