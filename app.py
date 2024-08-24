from fastapi import FastAPI
import logging
import os

log_level = os.environ.get("LOG_LEVEL", "ERROR").upper()

# Configure the logging
logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()


EMBEDDING_ENABLED = os.environ.get("EMBEDDING_ENABLED", "false").lower().strip()
EMBEDDING_ENABLED = EMBEDDING_ENABLED not in ["0", "false", "no"]

TRANSCRIPTION_ENABLED = os.environ.get("TRANSCRIPTION_ENABLED", "false").lower().strip()
TRANSCRIPTION_ENABLED = TRANSCRIPTION_ENABLED not in ["0", "false", "no"]

PLATFORM_ENABLED = os.environ.get("STRAICO_PLATFORM_ACCESS_TOKEN") is not None
