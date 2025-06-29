from fastapi.responses import JSONResponse
from fastapi import Request
from app import app, logging
import json

cached = app.cached
from backend import list_model, list_agents

from asyncio import gather

logger = logging.getLogger(__name__)


async def list_straico_models(api_key=None):
    models = await list_model(api_key)
    models = models["chat"]
    return [
        {
            "id": model["model"],
            "object": "model",
            "owned_by": model["name"].split(":")[0],
            "permission": [{}],
        }
        for model in models
    ]


async def list_agents_as_models(api_key=None):
    agents = await list_agents(api_key)
    if agents is not None and len(agents) > 0:
        return [
            {
                "id": f"agent/{m['name'].strip()}:{m['_id']}",  # m['name'],
                "object": "model",
                "owned_by": "Straico",
                "permission": [{}],
            }
            for m in agents
        ]

    return []


def list_auto_select_models():
    return [
        {
            "id": f"auto_select_model/balance:latest",  # m['name'],
            "object": "model",
            "owned_by": "Straico",
            "permission": [{}],
        },
        {
            "id": f"auto_select_model/budget:latest",  # m['name'],
            "object": "model",
            "owned_by": "Straico",
            "permission": [{}],
        },
        {
            "id": f"auto_select_model/quality:latest",  # m['name'],
            "object": "model",
            "owned_by": "Straico",
            "permission": [{}],
        },
    ]


@app.get("/api/models")
@app.get("/v1/api/models")
@app.get("/v1/models")
@app.get("/models")
@cached()
async def lmstudio_list_models(request: Request):
    """
     {'name': 'Anthropic: Claude 3 Haiku',
    'model': 'anthropic/claude-3-haiku:beta',
    'pricing': {'coins': 1, 'words': 100}}
    """
    api_key = request.headers.get("authorization")
    if api_key is not None:
        api_key = api_key[7:]
    models, agents = await gather(
        list_straico_models(api_key), list_agents_as_models(api_key)
    )
    models += agents
    models += list_auto_select_models()
    response = {"data": models, "object": "list"}
    return JSONResponse(content=response)
