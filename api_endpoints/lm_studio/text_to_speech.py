import json
import os

from fastapi import Request
from fastapi import UploadFile, Form, File
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from app import (
    app,
    logging,
    PLATFORM_ENABLED,
    TTS_PROVIDER,
    TTS_PROVIDER_LAZYBIRD,
    TTS_PROVIDER_STRAICO_PLATFORM,
)
from io import BytesIO

logger = logging.getLogger(__name__)

if TTS_PROVIDER == TTS_PROVIDER_LAZYBIRD:
    logger.info("TTS Provider set to Lazybird")
    from backend.lazybird import tts, tts_models

    voice_model_result = None
    voice_model_last_update_dt = None
    from datetime import timedelta, datetime

    async def get_model_mapping():
        global voice_model_last_update_dt, voice_model_result
        if (
            voice_model_last_update_dt is None
            or (voice_model_last_update_dt + timedelta(minutes=60)) <= datetime.now()
        ):
            voice_model_result = await tts_models()
            voice_model_last_update_dt = datetime.now()
        return voice_model_result

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
        model_list = await tts_models()
        model_ids = (m["id"] for m in model_list)
        if voice not in model_ids:
            model_mapping = dict(((m["displayName"], m["id"]) for m in model_list))
            if voice not in model_mapping:
                voice = os.environ.get(
                    "DEFAULT_LAZYBIRD_VOICE", "msa.en-US.AndrewMultilingual"
                )
            else:
                voice = model_mapping[voice]

        speech_content = await tts(input_text, voice, speed=speed)
        stream = BytesIO(speech_content)
        return StreamingResponse(stream, media_type="application/octet-stream")


if TTS_PROVIDER == TTS_PROVIDER_STRAICO_PLATFORM and PLATFORM_ENABLED:
    logger.info("TTS, STT Provider set to Straico Platform")
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
