import logging
import whisper
import pathlib
from fastapi import UploadFile, Form, File
from fastapi.responses import JSONResponse
from app import app
from typing import Optional
import tempfile
import asyncio
from os import environ

logger = logging.getLogger(__name__)

default_transcription_model = environ.get("DEFAULT_TRANSCRIPTION_MODEL", "base")

from multiprocessing import Process, Queue


def process_transcribe(queue, filename, model_name):
    model = whisper.load_model(model_name)
    result = model.transcribe(filename)
    queue.put(result["text"])


async def process_in_background(queue, filename, model_name):
    process = Process(target=process_transcribe, args=(queue, filename, model_name))
    process.start()

    while True:
        if not queue.empty():
            result = queue.get()
            process.join()
            return result
        await asyncio.sleep(5)


@app.post("/v1/audio/transcriptions")
async def lm_studio_transcriptions(
    file: UploadFile = File(...), model: Optional[str] = Form(None)
):
    contents = await file.read()
    model_name = default_transcription_model

    with tempfile.TemporaryDirectory() as tmpdirname:
        file = pathlib.Path(tmpdirname) / file.filename
        with file.open("wb") as writer:
            writer.write(contents)

        queue = Queue()
        text = await process_in_background(queue, str(file), model_name)
        return JSONResponse(content={"text": text})
