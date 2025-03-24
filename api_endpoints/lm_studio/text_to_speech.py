import json

from fastapi import Request
from fastapi import UploadFile, Form, File
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from app import app, logging, PLATFORM_ENABLED
from io import BytesIO
from os import environ

logger = logging.getLogger(__name__)

TTS_PROVIDER = environ.get("TTS_PROVIDER", "STRAICO_PLATFORM")

if TTS_PROVIDER == "LAZYBIRD":
    logger.info("TTS Provider set to Lazybird")
    from backend.lazybird import tts

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
        speed = post_json_data.get("speed", 1.0)

        speech_content = await tts(input_text, voice, speed=speed)
        stream = BytesIO(speech_content)
        return StreamingResponse(stream, media_type="application/octet-stream")


if TTS_PROVIDER == "STRAICO_PLATFORM" and PLATFORM_ENABLED:
    from backend.straico_platform import tts, download_file, stt

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

    @app.post("/v1/audio/transcriptions")
    async def lm_studio_stt(
        file: UploadFile = File(...), model: Optional[str] = Form(None)
    ):
        contents = await file.read()
        logger.debug(file.filename)
        text = await stt(contents, file.filename)
        return JSONResponse(content={"text": text})
