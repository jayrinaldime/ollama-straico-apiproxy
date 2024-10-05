try:
    from dotenv import load_dotenv

    load_dotenv()
except:
    pass
from os import environ

from app import (
    app,
    logging,
    log_level,
    TRANSCRIPTION_ENABLED,
    EMBEDDING_ENABLED,
    PLATFORM_ENABLED,
)
from api_endpoints.lm_studio import basic, chat, image
from api_endpoints.ollama import basic, chat

if PLATFORM_ENABLED:
    from api_endpoints.lm_studio import text_to_speech

if EMBEDDING_ENABLED:
    from api_endpoints.lm_studio import embedding
    from api_endpoints.ollama import embedding

if TRANSCRIPTION_ENABLED:
    from api_endpoints.lm_studio import speech_to_text

import uvicorn

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.info("Starting the web server")
    is_debug = log_level in ["INFO", "DEBUG"]
    HOST = environ.get("HOST", "0.0.0.0")
    PORT = int(environ.get("PORT", "3214"))
    uvicorn.run(app, host=HOST, port=PORT, log_level=log_level.lower())
