from os import environ
from app import logging

logger = logging.getLogger(__name__)

STRAICO_API_KEY = environ["STRAICO_API_KEY"]
logger.debug(f"STRAICO_API_KEY={STRAICO_API_KEY}")

if STRAICO_API_KEY.strip().upper() == "TEST":
    from .test import prompt_completion, list_model
    logger.info("Using Backend Test")
else:
    from .straico import prompt_completion, list_model
    logger.info("Using Backend Straico")