import base64
from os import environ
from typing import List

from app import logging
from const import VERSION, PROJECT_NAME
import platform
from datetime import datetime, timedelta
from aio_straico import aio_straico_client
from aio_straico.utils.tracing import observe
from aio_straico.api.v0 import ImageSize

from .straico_platform import autoerase_chat, autoerase_upload_image
from .straico_platform import models as platform_models
from datetime import timezone, datetime
from data.agent_data import chat_settings_read
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
        if model["pricing"]["coins"] == 0:
            continue
        _id = model["_id"], model["pricing"]["coins"]
        model_id_mapping[name] = _id
        model_id_mapping[model_name] = _id
    return model_id_mapping


async def agent_promp_completion(agent_id, msg):
    async with aio_straico_client(timeout=TIMEOUT) as client:
        settings = chat_settings_read(agent_id)

        response = await client.agent_prompt_completion(agent_id, msg, **settings)
        return response["answer"]


@observe
async def prompt_completion(
    msg: str,
    images=None,
    model: str = "openai/gpt-3.5-turbo-0125",
    temperature: float = None,
    max_tokens: float = None,
) -> str:
    # some  clients add :latest
    models = await get_model_mapping()
    model_values = [m["model"] for m in models]

    is_model_found = model in model_values

    if not is_model_found:
        if model.startswith("agent/"):  # lmstudio agent request
            model = model.split(":")[-1]
            return await agent_promp_completion(model, msg)
        elif model.startswith("Agent: "):  # Ollama agent request
            model = model.split("(")[-1][:-1]
            return await agent_promp_completion(model, msg)
        elif model.endswith(":latest"):
            model = model.replace(":latest", "")
            is_model_found = model in model_values

        if not is_model_found:
            model_name_mapping = dict(((m["name"], m["model"]) for m in models))
            if model in model_name_mapping:
                model = model_name_mapping[model]
                is_model_found = model in model_values

        if not is_model_found:
            model_alias = "ALIAS_" + model.upper().strip().replace("-", "_").replace(
                "/", "_"
            ).replace("  ", " ").replace(" ", "_").replace("__", "_")
            new_model = environ.get(model_alias)

            if new_model is not None:
                model = new_model.strip()
            else:
                logger.debug(
                    f"Unknown model {model}. Looking for alias model {model_alias}."
                )
                raise Exception(f"Unknown Model {model}")

    if not PLATFORM_ENABLED or images is None or len(images) == 0:
        post_request_data = {"model": model, "message": msg}
        logger.debug(f"Request Post Data: {post_request_data}")
        settings = {}
        if temperature is not None:
            settings["temperature"] = temperature
        if max_tokens is not None:
            settings["max_tokens"] = max_tokens
        async with aio_straico_client(timeout=TIMEOUT) as client:
            response = await client.prompt_completion(model, msg, **settings)
            logger.debug(f"response body: {response}")
            return response["completion"]["choices"][-1]["message"]["content"]
    else:
        platform_model_map = await get_platform_model_mapping()
        if model not in platform_model_map:
            split_index = model.find("/")
            new_model_name = model[split_index+1:]
            if new_model_name in platform_model_map:
                model = new_model_name
            else:
                logger.error(f"Model not found Platform [{model}, {new_model_name}]")
                raise Exception("Model not found in Platform")

        model_id, model_cost = platform_model_map[model]

        with TemporaryDirectory() as tmpdirname:
            local_image_path = []
            for index, image in enumerate(images):
                utc_now = datetime.now(timezone.utc)
                str_now = (
                    utc_now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + f"{index:03}Z.png"
                )
                pathfile = Path(tmpdirname) / str_now
                with pathfile.open("wb") as fp:
                    data = base64.urlsafe_b64decode(
                        image
                    )  # .standard_b64decode(images[0])
                    fp.write(data)
                local_image_path.append(pathfile)

            async with autoerase_upload_image(*local_image_path) as upload_stat:
                async with autoerase_chat(
                    model_id,
                    model_cost,
                    upload_stat,
                    msg,
                ) as chat_response:
                    return chat_response["message"]["data"]["content"]


async def list_model():
    async with aio_straico_client(timeout=TIMEOUT) as client:
        return await client.models(v=1)


async def list_rags():
    async with aio_straico_client(timeout=TIMEOUT) as client:
        return await client.rags()


async def delete_rag(rag_id: str):
    try:
        async with aio_straico_client(timeout=TIMEOUT) as client:
            # Assuming the method to delete a RAG is `client.delete_rag(rag_id)`
            result = await client.rag_delete(rag_id)
            return result
    except Exception as e:
        logger.error(f"Failed to delete RAG: {e}")
        raise


async def create_rag(
    name: str,
    description: str,
    file_to_uploads: List[Path],
    chunking_method: str = "fixed_size",
    chunk_size: int = 1000,
    chunk_overlap: int = 50,
    breakpoint_threshold_type: str = None,
    buffer_size: int = 500,
):
    try:
        async with aio_straico_client(timeout=TIMEOUT) as client:
            # Prepare RAG creation parameters
            kwargs = {
                "breakpoint_threshold_type": breakpoint_threshold_type,
                "buffer_size": buffer_size,
                "chunking_method": chunking_method,
                "chunk_size": chunk_size,
                "chunk_overlap": chunk_overlap,
            }

            # Call RAG creation method
            result = await client.create_rag(
                name, description, *file_to_uploads, **kwargs
            )

            return result.get("_id")  # Return the created RAG's ID

    except Exception as e:
        logger.error(f"Failed to create RAG: {e}")
        raise


async def list_agents():
    async with aio_straico_client(timeout=TIMEOUT) as client:
        return await client.agents()


async def delete_agent(agent_id):
    async with aio_straico_client(timeout=TIMEOUT) as client:
        agent = await client.agent_object(agent_id)
        r = await agent.delete()
        return r


async def create_agent(name, description, custom_prompt, model, rag_id, tags):
    async with aio_straico_client(timeout=TIMEOUT) as client:
        rags = {}
        if rag_id is not None and len(rag_id.strip()) > 0:
            rags["rag"] = rag_id
        result = await client.create_agent(
            name, description, model, custom_prompt, tags, **rags
        )

        return result.get("_id")  # Return the created RAG's ID


async def update_agent(agent_id, name, description, custom_prompt, model, rag_id, tags):
    async with aio_straico_client(timeout=TIMEOUT) as client:
        rags = {}
        if rag_id is not None and len(rag_id.strip()) > 0:
            rags["rag"] = rag_id

        result = await client.agent_update(
            agent_id,
            name=name,
            description=description,
            model=model,
            system_prompt=custom_prompt,
            tags=tags,
            **rags,
        )
        return result


async def user_detail():
    async with aio_straico_client(timeout=TIMEOUT) as client:
        return await client.user()


async def image_generation(model: str, n: int, prompt: str, size: ImageSize):
    async with aio_straico_client(timeout=TIMEOUT) as client:
        images = await client.image_generation(
            model=model,
            description=prompt,
            size=size,
            variations=n,
        )
        return images


async def update_agent_chat_settings(agent_id, chat_settings):
    async with aio_straico_client(timeout=TIMEOUT) as client:
        # Validate chat settings
        valid_search_types = {"similarity", "mmr", "similarity_score_threshold"}
        if chat_settings.get("search_type") not in valid_search_types:
            raise Exception(f"Invalid search type {chat_settings.get('search_type')}")

        # Ensure required fields are present
        if (
            chat_settings["search_type"] == "similarity"
            and chat_settings.get("k") is None
        ):
            raise Exception(
                "Number of documents (k) is required for similarity search."
            )
        elif chat_settings["search_type"] == "mmr" and (
            chat_settings.get("fetch_k") is None
            or chat_settings.get("lambda_mult") is None
        ):
            raise Exception(
                "Fetch K and Lambda Multiplier are required for MMR search."
            )
        elif (
            chat_settings["search_type"] == "similarity_score_threshold"
            and chat_settings.get("score_threshold") is None
        ):
            raise Exception(
                "Score Threshold is required for similarity score threshold search."
            )

        result = await client.agent_update(agent_id, chat_settings=chat_settings)
        return result
