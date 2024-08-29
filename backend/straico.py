import base64
from os import environ
from app import logging
from const import VERSION, PROJECT_NAME
import platform
from datetime import datetime, timedelta
from aio_straico import aio_straico_client
from aio_straico.api.v0 import ImageSize

from .straico_platform import autoerase_chat, autoerase_upload_image
from .straico_platform import models as platform_models
from datetime import timezone, datetime

from pathlib import Path
from tempfile import TemporaryDirectory

logger = logging.getLogger(__name__)

model_result = None
model_last_update_dt = None

platform_model_result = None
platform_model_last_update_dt = None

# CLIENT_USER_AGENT = f"{PROJECT_NAME}/{VERSION} ({platform.system()}; {platform.processor()};) py/{platform.python_version()}"
# logger.debug(f"Straico Client User Agent = {CLIENT_USER_AGENT}")

CACHE_MODEL_LIST = int(environ.get("STRAICO_CACHE_MODEL_LIST", "60"))
TIMEOUT = int(environ.get("STRAICO_TIMEOUT", "600"))

from app import PLATFORM_ENABLED


async def get_model_mapping():
    global model_last_update_dt, model_result
    if (
        model_last_update_dt is None
        or (model_last_update_dt + timedelta(minutes=CACHE_MODEL_LIST))
        <= datetime.now()
    ):
        model_result = await list_model()
        model_last_update_dt = datetime.now()

    models = model_result
    if models is None:
        return {}

    if "chat" in models:
        models = models["chat"]
    return models


async def get_platform_model_mapping():
    global platform_model_last_update_dt, platform_model_result
    if (
        platform_model_last_update_dt is None
        or (platform_model_last_update_dt + timedelta(minutes=CACHE_MODEL_LIST))
        <= datetime.now()
    ):
        platform_model_result = await model_listing()
        platform_model_last_update_dt = datetime.now()

    models = platform_model_result
    if models is None:
        return {}

    return models


async def model_listing():
    model_id_mapping = {}
    models = await platform_models()
    for model in models:
        name = model["name"]
        model_name = model["model"]
        _id = model["_id"], model["pricing"]["coins"]
        model_id_mapping[name] = _id
        model_id_mapping[model_name] = _id
    return model_id_mapping


async def prompt_completion(
    msg: str, images=None, model: str = "openai/gpt-3.5-turbo-0125"
) -> str:
    # some  clients add :latest
    models = await get_model_mapping()
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
    if not PLATFORM_ENABLED or images is None or len(images) == 0:
        post_request_data = {"model": model, "message": msg}
        logger.debug(f"Request Post Data: {post_request_data}")
        async with aio_straico_client(timeout=TIMEOUT) as client:
            response = await client.prompt_completion(model, msg)
            logger.debug(f"response body: {response}")
            return response["completion"]["choices"][-1]["message"]["content"]
    else:
        platform_model_map = await get_platform_model_mapping()
        if model.startswith("openai/"):
            model = model[7:]
        model_id, model_cost = platform_model_map[model]

        with TemporaryDirectory() as tmpdirname:

            utc_now = datetime.now(timezone.utc)
            str_now = utc_now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z.png"
            pathfile = Path(tmpdirname) / str_now
            with pathfile.open("wb") as fp:
                data = base64.urlsafe_b64decode(
                    images[0]
                )  # .standard_b64decode(images[0])
                fp.write(data)

            async with autoerase_upload_image(pathfile) as upload_stat:
                async with autoerase_chat(
                    model_id,
                    model_cost,
                    upload_stat["file"]["url"],
                    upload_stat["file"]["words"],
                    msg,
                ) as chat_response:
                    return chat_response["message"]["data"]["content"]


async def list_model():
    async with aio_straico_client(timeout=TIMEOUT) as client:
        return await client.models(v=1)


async def user_detail():
    async with aio_straico_client(timeout=TIMEOUT) as client:
        return await client.user()


async def image_generation(model: str, n: int, prompt: str, size: ImageSize, directory):
    async with aio_straico_client(timeout=TIMEOUT) as client:
        images = await client.image_generation_as_images(
            model=model,
            description=prompt,
            size=size,
            variations=n,
            destination_directory_path=directory,
        )
        return images
