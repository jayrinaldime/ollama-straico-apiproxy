from httpx import AsyncClient
from os import environ

STRAICO_PLATFORM_ACCESS_TOKEN = environ.get("STRAICO_PLATFORM_ACCESS_TOKEN")


async def tts(text, model="tts-1", voice="alloy"):
    text = text.strip()
    word_count = len(text.split())
    cost_per_model = {"tts-1": 0.04, "tts-1-hd": 0.08}
    cost = cost_per_model[model]
    cost *= word_count
    cost_str = str(int(cost * 100) / 100)

    async with AsyncClient() as session:
        response = await session.post(
            "https://platform.straico.com/api/file/tts",
            headers={"x-access-token": STRAICO_PLATFORM_ACCESS_TOKEN},
            json={"text": text, "voice": voice, "quality": model, "coins": cost_str},
            timeout=300,
        )
        response.raise_for_status()
        if response.json()["success"]:
            return response.json()["url"]


async def download_file(file_url):
    async with AsyncClient() as session:
        response = await session.get(file_url, timeout=300)
        response.raise_for_status()
        return response.content
