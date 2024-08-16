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
if EMBEDDING_ENABLED in ["0", "false", "no"]:
    EMBEDDING_ENABLED = False
else:
    EMBEDDING_ENABLED = True

TRANSCRIPTION_ENABLED = os.environ.get("TRANSCRIPTION_ENABLED", "false").lower().strip()
if TRANSCRIPTION_ENABLED in ["0", "false", "no"]:
    TRANSCRIPTION_ENABLED = False
else:
    TRANSCRIPTION_ENABLED = True
