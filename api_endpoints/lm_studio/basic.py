from fastapi.responses import JSONResponse
from app import app, logging
from backend import list_model, list_agents

from asyncio import gather

logger = logging.getLogger(__name__)


async def list_straico_models():
    models = await list_model()
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


async def list_agents_as_models():
    agents = await list_agents()
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
async def lmstudio_list_models():
    """
     {'name': 'Anthropic: Claude 3 Haiku',
    'model': 'anthropic/claude-3-haiku:beta',
    'pricing': {'coins': 1, 'words': 100}}
    """
    models, agents = await gather(list_straico_models(), list_agents_as_models())
    models += agents
    models += list_auto_select_models()
    response = {"data": models, "object": "list"}
    return JSONResponse(content=response)
