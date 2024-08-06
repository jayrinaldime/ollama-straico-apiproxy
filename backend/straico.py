import requests
from os import environ
from app import logging
from const import VERSION, PROJECT_NAME
import platform
from functools import lru_cache, wraps
from datetime import datetime, timedelta
from aio_straico import aio_straico_client

logger = logging.getLogger(__name__)

CLIENT_USER_AGENT = f"{PROJECT_NAME}/{VERSION} ({platform.system()}; {platform.processor()};) py/{platform.python_version()}"
logger.debug(f"Straico Client User Agent = {CLIENT_USER_AGENT}")

CACHE_MODEL_LIST = int(environ.get("STRAICO_CACHE_MODEL_LIST", "60"))
CACHE_USER = int(environ.get("STRAICO_CACHE_USER", "1"))

def timed_lru_cache(seconds: int, maxsize: int = 128):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.utcnow() + func.lifetime

        @wraps(func)
        async def wrapped_func(*args, **kwargs):
            if datetime.utcnow() >= func.expiration:
                func.cache_clear()
                func.expiration = datetime.utcnow() + func.lifetime
            return await func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


async def get_model_mapping():
    models = await list_model()
    if models is None:
        return {}

    if "chat" in models:
        models = models["chat"]
    return models


async def prompt_completion(msg: str, model: str = "openai/gpt-3.5-turbo-0125") -> str:
    # some  clients add :latest
    models = get_model_mapping()
    model_values = [m["model"] for m in models]

    is_model_found = model in model_values

    if not is_model_found:
        if model.endswith(":latest"):
            model = model.replace(":latest", "")
            is_model_found = model in model_values

        if not is_model_found:
            model_name_mapping = dict(((m["name"], m["model"]) for m in models))
            if model in model_name_mapping:
                model = model_name_mapping[model]
                is_model_found = model in model_values

        if not is_model_found:
            raise Exception(f"Unknown Model {model}")

    post_request_data = {"model": model, "message": msg}
    logger.debug(f"Request Post Data: {post_request_data}")
    async with aio_straico_client() as client:
        response = await client.prompt_completion(model, msg)
        logger.debug(f"response body: {response}")
        return response["completion"]["choices"][-1]["message"]["content"]


@timed_lru_cache(seconds=CACHE_MODEL_LIST * 60, maxsize=1)
async def list_model():
    async with aio_straico_client() as client:
        return await client.models(v=1)


@timed_lru_cache(seconds=CACHE_USER * 60, maxsize=1)
async def user_detail():
    async with aio_straico_client() as client:
        return await client.user()

