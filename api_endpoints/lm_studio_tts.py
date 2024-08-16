import json
import logging

from fastapi import Request
from fastapi.responses import StreamingResponse
from app import app
from backend.straico_platform import tts, download_file

from io import BytesIO
from os import environ

logger = logging.getLogger(__name__)

default_embedding_model = environ.get(
    "DEFAULT_EMBEDDING_MODEL", "nomic-ai/nomic-embed-text-v1.5"
)


@app.post("/v1/audio/speech")
async def lm_studio_tts(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    logger.debug(post_json_data)

    model = post_json_data["model"]
    input_text = post_json_data["input"]
    voice = post_json_data["voice"]

    speech_url = await tts(input_text, model, voice)
    if speech_url is None:
        return

    speech_blob = await download_file(speech_url)
    stream = BytesIO(speech_blob)
    return StreamingResponse(stream, media_type="application/octet-stream")
