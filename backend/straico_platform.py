from httpx import AsyncClient
from os import environ
from datetime import timezone, datetime

from contextlib import asynccontextmanager


STRAICO_PLATFORM_ACCESS_TOKEN = environ.get("STRAICO_PLATFORM_ACCESS_TOKEN")

PLATFORM_BASE_URL = "https://platform.straico.com/api"


@asynccontextmanager
async def autoerase_upload_image(image_path):
    try:
        size = image_path.stat().st_size

        img_url = await _upload(image_path)
        # pprint.pprint(img_url)

        upload_stat = await _file_upload(img_url["url"], image_path.name, size, "image")
        yield upload_stat
    finally:
        deleted = await _file_delete(upload_stat["file"]["_id"])


@asynccontextmanager
async def autoerase_chat(model_id, model_cost, img_url, img_words, text_prompt):
    try:
        chat_response = await _chat(
            model_id, model_cost, text_prompt, img_url, img_words
        )
        yield chat_response

    finally:
        delete_chat = await _delete_chat(chat_response["hash"])


async def models():
    async with AsyncClient() as session:
        response = await session.get(
            PLATFORM_BASE_URL + "/model",
            headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN},
            timeout=300,
        )
        response.raise_for_status()
        if response.json()["success"]:
            return response.json()["models"]


async def tts(text, model="tts-1", voice="alloy"):
    text = text.strip()
    word_count = _word_count(text)
    cost_per_model = {"tts-1": 0.04, "tts-1-hd": 0.08}
    cost = cost_per_model[model]
    cost *= word_count
    cost_str = str(int(cost * 100) / 100)

    async with AsyncClient() as session:
        response = await session.post(
            PLATFORM_BASE_URL + "/file/tts",
            headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN},
            json={"text": text, "voice": voice, "quality": model, "coins": cost_str},
            timeout=300,
        )
        response.raise_for_status()
        if response.json()["success"]:
            return response.json()["url"]


async def stt(binary_data, filename):
    files = {
        "file": (
            filename,
            binary_data,
            "audio/wav",  # "audio/mpeg",
        ),
    }

    async with AsyncClient() as session:
        response = await session.post(
            PLATFORM_BASE_URL + "/auth/whisper",
            headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN},
            files=files,
            timeout=300,
        )
        response.raise_for_status()
        if response.json():
            return response.json()["text"]


async def _upload(file_path):
    with file_path.open("rb") as binary_reader:
        binary_data = binary_reader.read(-1)

    filename = file_path.name
    content_type_mapping = {
        "jpeg": "image/jpeg",
        "jpg": "image/jpeg",
        "png": "image/png",
        "bmp": "image/bmp",
    }

    content_type = content_type_mapping[filename.split(".")[-1]]

    files = {"file": (filename, binary_data, content_type)}

    url = PLATFORM_BASE_URL + "/user/upload"

    async with AsyncClient() as session:
        response = await session.post(
            url, headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN}, files=files
        )
        if response.json()["success"]:
            return response.json()


async def _file_delete(image_id):
    url = PLATFORM_BASE_URL + "/file/visible"
    body_json = {"hash": image_id, "visible": False}
    async with AsyncClient() as session:
        response = await session.put(
            url,
            headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN},
            json=body_json,
        )

        return response.json()


async def _file_upload(document_url, document_name, document_size, document_type):
    url = PLATFORM_BASE_URL + "/file"
    body_json = {
        "url": document_url,
        "name": document_name,
        "size": document_size,
        "enabled": True,
        "type": document_type,
    }

    async with AsyncClient() as session:
        response = await session.post(
            url,
            headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN},
            json=body_json,
        )

        if response.json()["success"]:
            return response.json()


def _word_count(text):
    word_count = len(text.split())

    return word_count


async def download_file(file_url):
    async with AsyncClient() as session:
        response = await session.get(file_url, timeout=300)
        response.raise_for_status()
        return response.content


async def _chat(model_id, model_cost, text_prompt, image_url, image_word):
    utc_now = datetime.now(timezone.utc)
    str_now = utc_now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    word_count = _word_count(text_prompt)
    prompt_cost = word_count + image_word

    cost_str = str(int(model_cost * prompt_cost * 100) / 100)
    async with AsyncClient() as session:
        response = await session.post(
            PLATFORM_BASE_URL + "/ai/chat",
            headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN},
            json={
                "message": [
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "words": image_word},
                    },
                    {"type": "text", "text": text_prompt},
                ],
                "hash": None,
                "date": str_now,
                "files": None,
                "idModel": [model_id],
                "coins": cost_str,
                "params": {},
                "behaviours": [],
                "currentPrompt": None,
                "capabilities": [],
            },
            timeout=300,
        )
        response.raise_for_status()
        if response.json():
            return response.json()


async def _delete_chat(chat_hash):
    async with AsyncClient() as session:
        response = await session.delete(
            PLATFORM_BASE_URL + f"/chat/{chat_hash}",
            headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN},
        )
        response.raise_for_status()
        if response.json():
            return response.json()
