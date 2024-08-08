from os import environ
from app import logging

logger = logging.getLogger(__name__)

STRAICO_API_KEY = environ["STRAICO_API_KEY"]
logger.debug(f"STRAICO_API_KEY={STRAICO_API_KEY}")

if STRAICO_API_KEY.strip().upper() == "TEST":
    from .test import prompt_completion, list_model, user_detail

    logger.info("Using Test Backend")
else:
    from .straico import prompt_completion, list_model, user_detail, image_generation

    logger.info("Using Straico Backend")
