import json
import os

from fastapi import Request
from fastapi import UploadFile, Form, File
from fastapi.responses import StreamingResponse, JSONResponse
from typing import Optional
from app import (
    app,
    logging
)
from io import BytesIO
logger = logging.getLogger(__name__)
from backend.lazybird import LAZYBIRD_API_KEY

if LAZYBIRD_API_KEY is not None:
    logger.info("TTS Lazybird Enabled")
    from backend.lazybird import (tts as tts_lazybird, tts_models as tts_models_lazybird)

    voice_model_result_lazybird = None
    voice_model_last_update_dt_lazybird = None
    from datetime import timedelta, datetime

    async def get_lazybird_model_mapping():
        global voice_model_last_update_dt_lazybird, voice_model_result_lazybird
        if (
            voice_model_last_update_dt_lazybird is None
            or (voice_model_last_update_dt_lazybird + timedelta(minutes=60)) <= datetime.now()
        ):
            result = await tts_models_lazybird()
            ids = (m["id"] for m in result)
            name_mapping = dict(((m["displayName"], m["id"]) for m in result))
            voice_model_last_update_dt_lazybird = datetime.now()
            voice_model_result_lazybird = ids, name_mapping
        return voice_model_result_lazybird

    @app.post("/v1/lazybird/audio/speech")
    async def lazybird_tts(request: Request):
        try:
            post_json_data = await request.json()
        except:
            post_json_data = json.loads((await request.body()).decode())
        logger.debug(post_json_data)

        input_text = post_json_data["input"]
        voice = post_json_data["voice"]
        speed = post_json_data.get("speed", 1.0)
        ids, model_mapping = await get_lazybird_model_mapping()

        if voice not in ids:
            if voice not in model_mapping:
                voice = os.environ.get(
                    "DEFAULT_LAZYBIRD_VOICE", "msa.en-US.AndrewMultilingual"
                )
            else:
                voice = model_mapping[voice]

        speech_content = await tts_lazybird(input_text, voice, speed=speed)
        stream = BytesIO(speech_content)
        return StreamingResponse(stream, media_type="application/octet-stream")




from backend.straico import tts_openai, tts_elevenlabs, elevenlabs_voices
from backend.straico_platform import download_file

@app.post("/v1/audio/speech")
@app.post("/v1/openai/audio/speech")
async def openai_tts(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    logger.debug(post_json_data)

    input_text = post_json_data["input"]
    voice = post_json_data["voice"]

    speech_url = await tts_openai(voice, input_text)
    if speech_url is None:
        return

    speech_blob = await download_file(speech_url["audio"])
    stream = BytesIO(speech_blob)
    return StreamingResponse(stream, media_type="application/octet-stream")


voice_model_result_elevenlabs = None
voice_model_last_update_dt_elevenlabs = None

async def get_elevenlabs_model_mapping():
    global voice_model_last_update_dt_elevenlabs, voice_model_result_elevenlabs
    if (
        voice_model_last_update_dt_elevenlabs is None
        or (voice_model_last_update_dt_elevenlabs + timedelta(minutes=60)) <= datetime.now()
    ):
        result = await elevenlabs_voices()
        voice_model_last_update_dt_elevenlabs = datetime.now()
        ids = (m["voice_id"] for m in result["voices"])
        name_mapping = dict(((m["name"], m["voice_id"]) for m in result["voices"]))
        voice_model_result_elevenlabs = ids, name_mapping
    return voice_model_result_elevenlabs
@app.post("/v1/elevenlabs/audio/speech")
async def elevenlabs_tts(request: Request):
    try:
        post_json_data = await request.json()
    except:
        post_json_data = json.loads((await request.body()).decode())
    logger.debug(post_json_data)

    input_text = post_json_data["input"]
    voice = post_json_data["voice"]
    ids, model_mapping = await get_elevenlabs_model_mapping()
    if voice not in ids:
        if voice not in model_mapping:
            voice = os.environ.get(
                "DEFAULT_ELEVENLABS_VOICE", "9BWtsMINqrJLrRacOk9x"
            )
        else:
            voice = model_mapping[voice]

    speech_url = await tts_elevenlabs(voice, input_text)
    if speech_url is None:
        return

    speech_blob = await download_file(speech_url["audio"])
    stream = BytesIO(speech_blob)
    return StreamingResponse(stream, media_type="application/octet-stream")
