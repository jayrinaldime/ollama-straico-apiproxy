import asyncio

from httpx import AsyncClient
from os import environ

LAZYBIRD_API_KEY = environ.get("LAZYBIRD_API_KEY")

LAZYBIRD_BASE_URL = environ.get("LAZYBIRD_BASE_URL", "https://api.lazybird.app/v1")


async def tts_models():
    list_voices_url = LAZYBIRD_BASE_URL + "/voices"
    async with AsyncClient() as session:
        response = await session.get(
            list_voices_url,
            headers={"X-API-Key": LAZYBIRD_API_KEY},
            timeout=300,
        )

        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        return None


async def tts(
    text, voice_id="msa.en-US.AndrewMultilingual", speed=1.0, pitch=1.0, style=None
):
    text = text.strip()
    settings = {
        "pitch": pitch,
        "speed": speed,
    }
    if style is not None:
        settings["style"] = style

    generate_speech_url = LAZYBIRD_BASE_URL + "/generate-speech"

    async with AsyncClient() as session:
        response = await session.post(
            generate_speech_url,
            headers={"X-API-Key": LAZYBIRD_API_KEY},
            json={"voiceId": voice_id, "text": text, "settings": settings},
            timeout=300,
        )

        response.raise_for_status()
        if response.status_code == 200:
            return response.content
        return None
