from os import environ
from app import logging

logger = logging.getLogger(__name__)

STRAICO_API_KEY = environ.get("STRAICO_API_KEY", "PER_REQUEST")
logger.debug(f"STRAICO_API_KEY={STRAICO_API_KEY}")

if STRAICO_API_KEY.strip().upper() == "TEST":
    from .test import (
        prompt_completion,
        list_model,
        user_detail,
        list_agents,
        create_agent,
        delete_agent,
        list_rags,
        delete_rag,
        create_rag,
        update_agent,
        get_errors,
    )
    from .straico import get_model_mapping

    logger.info("Using Test Backend")
elif STRAICO_API_KEY.strip().upper() == "PER_REQUEST":
    from .test import (
        user_detail,
        list_agents,
        create_agent,
        delete_agent,
        list_rags,
        delete_rag,
        create_rag,
        update_agent,
        get_errors,
    )

    from .straico import (
        prompt_completion,
        list_model,
        list_agents,
        elevenlabs_voices,
        image_generation,
        get_model_mapping,
    )

    logger.info("Using Straico Backend Per Request")
else:
    from .straico import (
        prompt_completion,
        list_model,
        elevenlabs_voices,
        list_agents,
        delete_agent,
        user_detail,
        image_generation,
        list_rags,
        delete_rag,
        create_rag,
        get_model_mapping,
        create_agent,
        update_agent,
        get_errors,
    )

    logger.info("Using Straico Backend")
